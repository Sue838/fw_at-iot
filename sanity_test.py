def test_sanity(get_sensor_info, get_sensor_reading, get_sensor_methods, set_sensor_name, set_sensor_reading_interval, reset_sensor_to_factory, update_sensor_firmware, sensor_reboot):
    sensor_info = get_sensor_info()
    """"set_sensor_name("new-name")
    sensor_methods = get_sensor_methods()
    set_sensor_reading_interval("5")
    reset_to_factory = reset_sensor_to_factory()
    update_firmware = update_sensor_firmware()
    reboot = sensor_reboot()"""
    sensor_name = sensor_info.get("name")
    assert isinstance(sensor_name, str), "Sensor name is not a string"

    sensor_hid = sensor_info.get("hid")
    assert isinstance(sensor_hid, str), "Sensor hid is not a string"

    sensor_model = sensor_info.get("model")
    assert isinstance(sensor_model, str), "Sensor model is not a string"

    sensor_firmware_version = sensor_info.get("firmware_version")
    assert isinstance(sensor_firmware_version, int), "Sensor firmware version is not an int"

    sensor_reading_interval = sensor_info.get("reading_interval")
    assert isinstance(sensor_reading_interval, int), "Sensor reading interval is not a string"

    sensor_reading = get_sensor_reading()
    assert isinstance(sensor_reading, float), "Sensor doesn't seem to register temperature"

    print("Sanity test passed")

