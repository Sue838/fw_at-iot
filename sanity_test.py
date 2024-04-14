def test_sanity(get_sensor_info, get_sensor_reading):
    
    sensor_info = get_sensor_info()
   
    sensor_name = sensor_info.name
    assert isinstance(sensor_name, str), "Sensor name is not a string"

    sensor_hid = sensor_info.hid
    assert isinstance(sensor_hid, str), "Sensor hid is not a string"

    sensor_model = sensor_info.model
    assert isinstance(sensor_model, str), "Sensor model is not a string"

    sensor_firmware_version = sensor_info.firmware_version
    assert isinstance(sensor_firmware_version, int), "Sensor firmware version is not an int"

    sensor_reading_interval = sensor_info.reading_interval
    assert isinstance(sensor_reading_interval, int), "Sensor reading interval is not a string"

    sensor_reading = get_sensor_reading()
    assert isinstance(sensor_reading, float), "Sensor doesn't seem to register temperature"

    print("Sanity test passed")

