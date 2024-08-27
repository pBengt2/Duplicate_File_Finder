"""
 This file is doing blah blah blah

"""

PLANT_CATALOG_FILE_PATH = r"C:\Users\Peter\Downloads\plant_catalog.xml"


def read_plant_catalog_file(xml_filename):
    common_names = []
    botanical_names = []
    zones = []
    lights = []
    prices = []
    with open(xml_filename) as xml_file:
        while True:
            line = xml_file.readline()
            if len(line) == 0:
                break
            parsed_line = line.split(">")[1].split("<")[0]
            if "COMMON" in line:
                common_names.append(parsed_line)
            elif "BOTANICAL" in line:
                botanical_names.append(parsed_line)
            elif "ZONE" in line:
                zones.append(parsed_line)
            elif "LIGHT" in line:
                lights.append(parsed_line)
            elif "PRICE" in line:
                prices.append(float(parsed_line.split("$")[1]))
    return common_names, botanical_names, zones, lights, prices


def display_arrays(common_names, botanical_names, zones, lights, prices):
    for index in range(len(common_names)):
        common_name = common_names[index]
        botanical_name = botanical_names[index]
        zone = zones[index]
        light = lights[index]
        price = prices[index]
        print("TODO: format printing")
        print(common_name)


def get_average(prices):
    average = sum(prices) / len(prices)
    return average


def display_prices(prices):
    prices_sum = sum(prices)
    prices_count = len(prices)
    prices_average = get_average(prices)
    print(prices_sum)
    print(prices_count)
    print(prices_average)


def main():
    catalog = PLANT_CATALOG_FILE_PATH
    common_names, botanical_names, zones, lights, prices = read_plant_catalog_file(catalog)

    display_arrays(common_names, botanical_names, zones, lights, prices)
    display_prices(prices)
    """
    common = parse_plant_data(xml_data, "COMMON")
    botanical = parse_plant_data(xml_data, "BOTANICAL")
    zone = parse_plant_data(xml_data, "ZONE")
    light = parse_plant_data(xml_data, "LIGHT")
    price = parse_plant_data(xml_data, "PRICE")
    
    info = display_arrays(common,botanical,zone,light,price)
    average = get_average()
    display_prices(total, average, count)
    """


main()
