
from django.urls import path
# from app.controllers.fcm_controller import send_notification_to_token
# from app.controllers.notifications import notify_user,save_fcm_token
from app.controllers.In_app_notifications import NotificationList

urlpatterns = [
    # path('notify_user/', notify_user, name='notify_user'),
    # path('save_fcm_token/', save_fcm_token, name='save_fcm_token'),4
    # path('send-notification-to-token/', send_notification_to_token, name='send_notification_to_token'),
    path('all_notifications/<int:pk>/', NotificationList.as_view(), name='notification-list'),
    # path('notifications_create/', NotificationCreate.as_view(), name='notification-create'),

]