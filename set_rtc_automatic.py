import rclpy
from rclpy.node import Node
from tier4_rtc_msgs.srv import AutoModeWithModule
import sys

class AutoModeClient(Node):

    def __init__(self, enable):
        super().__init__('auto_mode_client')
        self.client = self.create_client(AutoModeWithModule, '/api/external/set/rtc_auto_mode')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.send_request(enable)

    def send_request(self, enable):
        for module_type in range(1, 15):  # 1から14までの全てのmodule.typeでループ
            request = AutoModeWithModule.Request()
            request.module.type = module_type
            request.enable = enable
            self.future = self.client.call_async(request)
            rclpy.spin_until_future_complete(self, self.future)
            if self.future.result() is not None:
                self.get_logger().info(f'Service call succeeded for module type {module_type}')
            else:
                self.get_logger().error(f'Service call failed for module type {module_type}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv) < 2:
        print("Usage: call.py [auto|manual]")
        return
    mode = sys.argv[1]
    enable = True if mode == 'auto' else False
    auto_mode_client = AutoModeClient(enable)
    # rclpy.spin(auto_mode_client) を削除
    auto_mode_client.destroy_node()  # ノードを破棄

if __name__ == '__main__':
    main()
