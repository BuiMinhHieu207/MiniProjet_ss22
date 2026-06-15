import logging


def show_devices(devices):
    """
    Hiển thị danh sách thiết bị.
    """
    if not devices:
        print("Hệ thống chưa có thiết bị nào.")
        return

    print("\n{:<8}{:<25}{:<12}{:<12}{:<12}".format(
        "ID",
        "Location",
        "Old Index",
        "New Index",
        "Status"
    ))

    print("-" * 70)

    for device in devices:
        print(
            f"{device['id']:<8}"
            f"{device['location']:<25}"
            f"{device['old_index']:<12}"
            f"{device['new_index']:<12}"
            f"{device['status']:<12}"
        )


def find_device(devices, device_id):
    """
    Tìm thiết bị theo mã.
    """
    for device in devices:
        if device["id"].upper() == device_id.upper():
            return device

    return None


def input_non_negative_number(message):
    """
    Nhập số >= 0.
    """
    while True:
        try:
            value = int(input(message))

            if value < 0:
                print("Giá trị phải >= 0.")
                continue

            return value

        except ValueError:
            print("Vui lòng nhập số hợp lệ!")


def update_indices(devices):
    """
    Cập nhật chỉ số điện.
    """
    device_id = input("Nhập mã thiết bị: ").strip()

    device = find_device(devices, device_id)

    if device is None:
        print("ERR-E01: Không tìm thấy thiết bị.")
        return

    old_index = input_non_negative_number(
        "Nhập chỉ số cũ: "
    )

    while True:
        new_index = input_non_negative_number(
            "Nhập chỉ số mới: "
        )

        if new_index < old_index:
            print(
                "ERR-E02: Chỉ số mới "
                "phải >= chỉ số cũ."
            )
        else:
            break

    device["old_index"] = old_index
    device["new_index"] = new_index

    logging.info(
        "Updated indices for %s",
        device_id
    )

    print("Cập nhật thành công!")


def activate_overload_warning(devices):
    """
    Kích hoạt cảnh báo quá tải.
    """
    device_id = input(
        "Nhập mã thiết bị: "
    ).strip()

    device = find_device(
        devices,
        device_id
    )

    if device is None:
        print("ERR-E01: Không tìm thấy thiết bị.")
        return

    if device["status"] == "Overload":
        print(
            "ERR-E04: Thiết bị đã "
            "ở trạng thái Overload."
        )
        return

    consumption = (
        device["new_index"]
        - device["old_index"]
    )

    if consumption > 5000:
        device["status"] = "Overload"

        logging.warning(
            "Overload activated for %s",
            device_id
        )

        print(
            "Đã kích hoạt trạng thái "
            "Overload."
        )
    else:
        print(
            "Thiết bị chưa vượt "
            "ngưỡng 5000 kWh."
        )


def calculate_energy_financials(devices):
    """
    Trả về:
    (
        total_consumption,
        discount_percent,
        final_cost
    )
    """
    total_consumption = 0

    for device in devices:
        total_consumption += (
            device["new_index"]
            - device["old_index"]
        )

    total_cost = total_consumption * 3000

    discount_percent = 0

    if total_consumption >= 50000:
        discount_percent = 3

    final_cost = int(
        total_cost *
        (100 - discount_percent)
        / 100
    )

    return (
        total_consumption,
        discount_percent,
        final_cost
    )


def show_financial_report(devices):
    """
    Hiển thị báo cáo tài chính.
    """
    (
        total_consumption,
        discount_percent,
        final_cost
    ) = calculate_energy_financials(
        devices
    )

    print("\n===== BÁO CÁO NĂNG LƯỢNG =====")

    print(
        f"Tổng điện tiêu thụ: "
        f"{total_consumption:,} kWh"
    )

    print(
        f"Chiết khấu áp dụng: "
        f"{discount_percent}%"
    )

    print(
        f"Tổng tiền sau giảm giá: "
        f"{final_cost:,} VND"
    )


def display_menu():
    """
    Hiển thị menu.
    """
    print("\n===== ENERGY SYSTEM =====")
    print("1. Xem danh sách thiết bị")
    print("2. Cập nhật chỉ số điện")
    print("3. Kích hoạt cảnh báo")
    print("4. Tính tiền điện")
    print("5. Thoát")
    print("=========================")


def main():
    """
    Hàm chính.
    """
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s - "
            "%(levelname)s - "
            "%(message)s"
        )
    )

    devices = [
        {
            "id": "M01",
            "location":
                "Mechanical Shop A",
            "old_index": 1200,
            "new_index": 4500,
            "status": "Normal"
        },
        {
            "id": "M02",
            "location":
                "Assembly Line B",
            "old_index": 2300,
            "new_index": 8500,
            "status": "Overload"
        }
    ]

    while True:
        display_menu()

        try:
            choice = int(
                input(
                    "Chọn chức năng (1-5): "
                )
            )

            if choice == 1:
                show_devices(devices)

            elif choice == 2:
                update_indices(devices)

            elif choice == 3:
                activate_overload_warning(
                    devices
                )

            elif choice == 4:
                show_financial_report(
                    devices
                )

            elif choice == 5:
                print(
                    "Cảm ơn bạn đã "
                    "sử dụng hệ thống!"
                )
                break

            else:
                print(
                    "Lựa chọn không hợp lệ!"
                )

        except ValueError:
            print(
                "Vui lòng nhập số!"
            )


if __name__ == "__main__":
    main()
