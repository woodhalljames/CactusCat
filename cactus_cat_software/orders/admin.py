from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["service_package", "quantity", "price", "get_total_price"]
    can_delete = False

    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = "Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = [
        "order_number",
        "customer_name",
        "customer_email",
        "service_package",
        "total_amount",
        "status_badge",
        "created",
    ]
    list_filter = ["status", "created", "service_package__category"]
    search_fields = [
        "order_number",
        "customer_email",
        "customer_name",
        "company_name",
    ]
    readonly_fields = ["order_number", "created", "modified", "total_amount"]
    date_hierarchy = "created"
    actions = ["approve_orders", "mark_in_progress", "mark_completed", "convert_to_project"]

    fieldsets = (
        (
            "Order Information",
            {
                "fields": ("order_number", "status", "created", "modified"),
            },
        ),
        (
            "Customer Information",
            {
                "fields": (
                    "user",
                    "customer_name",
                    "customer_email",
                    "customer_phone",
                    "company_name",
                ),
            },
        ),
        (
            "Service Details",
            {
                "fields": ("service_package", "total_amount", "custom_requirements"),
            },
        ),
        (
            "Internal",
            {
                "fields": ("admin_notes",),
                "classes": ("collapse",),
            },
        ),
    )

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of orders
        return False

    def status_badge(self, obj):
        """Display status with color-coded badge."""
        colors = {
            "pending": "warning",
            "confirmed": "info",
            "in_progress": "primary",
            "completed": "success",
            "cancelled": "danger",
        }
        color = colors.get(obj.status, "secondary")
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"

    @admin.action(description="Approve selected orders")
    def approve_orders(self, request, queryset):
        """Approve pending orders."""
        updated = queryset.filter(status="pending").update(status="confirmed")
        self.message_user(
            request,
            f"{updated} order(s) approved and status changed to 'Confirmed'.",
        )

    @admin.action(description="Mark as In Progress")
    def mark_in_progress(self, request, queryset):
        """Mark orders as in progress."""
        updated = queryset.exclude(status__in=["completed", "cancelled"]).update(
            status="in_progress"
        )
        self.message_user(
            request,
            f"{updated} order(s) marked as 'In Progress'.",
        )

    @admin.action(description="Mark as Completed")
    def mark_completed(self, request, queryset):
        """Mark orders as completed."""
        updated = queryset.exclude(status="cancelled").update(status="completed")
        self.message_user(
            request,
            f"{updated} order(s) marked as 'Completed'.",
        )

    @admin.action(description="Convert to Project")
    def convert_to_project(self, request, queryset):
        """Convert selected orders into projects."""
        from cactus_cat_software.projects.models import Project

        created = 0
        skipped = 0
        errors = []

        for order in queryset:
            # Check if order already has a project
            if hasattr(order, 'project'):
                skipped += 1
                errors.append(f"Order {order.order_number} already has a project")
                continue

            # Check if order has a user
            if not order.user:
                skipped += 1
                errors.append(f"Order {order.order_number} has no associated user")
                continue

            # Create project
            try:
                # Determine project name from service package or items
                if order.service_package:
                    project_name = f"{order.service_package.name} - {order.customer_name}"
                elif order.items.exists():
                    first_item = order.items.first()
                    project_name = f"{first_item.service_package.name} - {order.customer_name}"
                else:
                    project_name = f"Project for {order.customer_name}"

                Project.objects.create(
                    order=order,
                    client=order.user,
                    project_name=project_name,
                    status="planning",
                    progress_percentage=0,
                )

                # Update order status if it's still pending
                if order.status == "pending":
                    order.status = "confirmed"
                    order.save()

                created += 1
            except Exception as e:
                skipped += 1
                errors.append(f"Order {order.order_number}: {str(e)}")

        # Show success message
        if created > 0:
            self.message_user(
                request,
                f"Successfully converted {created} order(s) to projects.",
                messages.SUCCESS,
            )

        # Show errors if any
        if errors:
            self.message_user(
                request,
                f"{skipped} order(s) skipped: " + "; ".join(errors[:5]),
                messages.WARNING,
            )
