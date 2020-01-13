import uuid
import xml.etree.ElementTree as xml
from datetime import datetime, timedelta
from tools.tools import format_hours

xmlms = {'base': "http://www.iaea.org/2012/IRIX/Format/Base",
         'html': "http://www.w3.org/1999/xhtml",
         'id': "http://www.iaea.org/2012/IRIX/Format/Identification",
         'irix': "http://www.iaea.org/2012/IRIX/Format",
         'loc': "http://www.iaea.org/2012/IRIX/Format/Locations",
         'mon': "http://www.iaea.org/2012/IRIX/Format/Measurements"}


def format_header():
    root = xml.Element("irix:Report")
    root.attrib["version"] = "1.0"
    for key, value in xmlms.items():
        root.attrib['xmlns:' + key] = value
    return root


def combine_xml(root: xml.Element, trees: list):
    first = root
    for tree in trees:
        data = tree.getroot()
        first.append(data)
    final_tree = xml.ElementTree(first)
    return final_tree


def format_time(given_time):
    date = str(given_time.date())
    time = str(given_time.strftime("%X"))
    return date + "T" + time + "Z"


def format_identification_subtree(file):
    file_data = xml.parse(file)

    id_root = xml.Element("id:Identification")
    org_reporting = xml.SubElement(id_root, "id:OrganisationReporting").text = file_data.find(
        "OrganisationReporting").text
    time = format_time(datetime.now())
    report_datetime = xml.SubElement(id_root, "id:DateAndTimeOfCreation").text = str(time)
    report_context = xml.SubElement(id_root, "id:ReportContext").text = file_data.find("ReportContext").text
    report_sequence_number = xml.SubElement(id_root, "id:SequenceNumber").text = file_data.find(
        ".//SequenceNumber").text
    report_uuid = xml.SubElement(id_root, "id:ReportUUID").text = str(uuid.uuid4())
    confidentiality = xml.SubElement(id_root, "id:Confidentiality").text = file_data.find("Confidentiality").text
    addresses = xml.SubElement(id_root, "id:Addressees")
    addressee = xml.SubElement(addresses, "id:Addressee").text = file_data.find(".//Addressee").text

    reporting_bases = xml.SubElement(id_root, "id:ReportingBases")
    reporting_basis = xml.SubElement(reporting_bases, "id:ReportingBasis").text = file_data.find(
        ".//ReportingBasis").text
    contact_person = xml.SubElement(id_root, "id:ContactPerson").text = file_data.find(".//ContactPerson").text

    identifications_fields = xml.SubElement(id_root, "id:Identifications")

    person_info = xml.SubElement(identifications_fields, "base:PersonContactInfo")
    name = xml.SubElement(person_info, "base:Name").text = file_data.findall(".//Name")[0].text
    userID = xml.SubElement(person_info, "base:UserID").text = file_data.find(".//UserID").text
    position = xml.SubElement(person_info, "base:Position").text = file_data.find(".//Position").text
    organisation_id = xml.SubElement(person_info, "base:OrganisationID").text = file_data.findall(
        ".//OrganisationID")[0].text

    org_contacts_info = xml.SubElement(identifications_fields, "base:OrganisationContactInfo")
    org_name = xml.SubElement(org_contacts_info,
                              "base:Name").text = file_data.findall(".//Name")[1].text
    org_id = xml.SubElement(org_contacts_info, "base:OrganisationID").text = file_data.findall(
        ".//OrganisationID")[1].text
    org_country = xml.SubElement(org_contacts_info, "base:Country").text = file_data.find(".//Country").text
    org_phone_number = xml.SubElement(org_contacts_info, "base:PhoneNumber").text = file_data.find(
        ".//PhoneNumber").text
    org_fax_number = xml.SubElement(org_contacts_info, "base:FaxNumber").text = file_data.find(".//FaxNumber").text

    id_tree = xml.ElementTree(id_root)
    return id_tree


def hardcode_identification_subtree():
    '''
        The create_id_xml creates the Identification xml tree according to the out from outer file. If the file is
        damaged or deleted the default filling of the tree goes here
        '''
    id_root = xml.Element("id:Identification")
    org_reporting = xml.SubElement(id_root, "id:OrganisationsReporting").text = "meteo.gov.ua"
    time = datetime.now()
    report_datetime = xml.SubElement(id_root, "id:DateAndTimeOfCreation").text = str(time)
    report_context = xml.SubElement(id_root, "id:ReportContext").text = "Routine"
    report_uuid = xml.SubElement(id_root, "id:ReportUUID").text = str(uuid.uuid4())
    confidentiality = xml.SubElement(id_root, "id:Confidentiality").text = "For Authority Use Only"
    identifications_fields = xml.SubElement(id_root, "id:Identifications")

    person_info = xml.SubElement(identifications_fields, "base:PersonContactInfo")
    name = xml.SubElement(person_info, "base:Name").text = "Leonid Tabachnyi"
    org_person_id = xml.SubElement(person_info, "base:OrganisationID").text = "tabachnyi@meteo.gov.ua"
    email = xml.SubElement(person_info, "base:EmailAdress").text = "380442399353"

    org_contacts_info = xml.SubElement(identifications_fields, "base:OrganisationContactInfo")
    org_name = xml.SubElement(org_contacts_info,
                              "base:Name").text = "Radiation Accidents Consequences Prediction Center"
    org_id = xml.SubElement(org_contacts_info, "base:OrganisationInfo").text = "meteo.gov.ua"
    org_country = xml.SubElement(org_contacts_info, "base:Country").text = "UA"
    org_phone_number = xml.SubElement(org_contacts_info, "base:PhoneNumber").text = "380442399353"
    org_fax_number = xml.SubElement(org_contacts_info, "base:FaxNumber").text = "380442796680"
    org_email = xml.SubElement(org_contacts_info, "base:EmailAddress").text = "ceprac@meteo.gov.ua"
    org_description = xml.SubElement(org_contacts_info, "base:Descrition").text = "Data originator for this report"

    org1_contacts_info = xml.SubElement(identifications_fields, "base:OrganisationContactInfo")
    org1_name = xml.SubElement(org1_contacts_info, "base:Name").text = "Ukrainian Hydrometeorological Center"
    org1_id = xml.SubElement(org1_contacts_info, "base:OrganisationID").text = "meteo.gov.ua"
    org1_country = xml.SubElement(org1_contacts_info, "base:Country").text = "UA"
    org1_phone_number = xml.SubElement(org1_contacts_info, "base:PhoneNumber").text = "380442399387"
    org1_fax_number = xml.SubElement(org1_contacts_info, "base:FaxNUmber").text = "380442791080"
    org1_email = xml.SubElement(org1_contacts_info, "base:EmailAddress").text = "office@meteo.gov.ua"
    org1_description = xml.SubElement(org1_contacts_info, "base:Description").text = "Data originator for this report"
    id_tree = xml.ElementTree(id_root)
    return id_tree


def format_measurements_subtree(measurements_list, end_measuring_timestamp):
    start_datetime = end_measuring_timestamp - timedelta(hours=1)
    end_datetime = end_measuring_timestamp
    measurement_root = xml.Element("mon:Measurements", ValidAt=format_time(end_datetime + timedelta(minutes=5)))
    dose_rate = xml.SubElement(measurement_root, "mon:DoseRateType").text = "Gamma"
    measurement_period = xml.SubElement(measurement_root, "mon:MeasuringPeriod")
    start_m_time = xml.SubElement(measurement_period, "mon:StartTime").text = format_time(start_datetime)
    end_m_time = xml.SubElement(measurement_period, "mon:EndTime").text = format_time(end_datetime)
    measurements = xml.SubElement(measurement_root, "mon:Measurements")
    for measurement_element in measurements_list:
        for index_key, measurement_value in measurement_element.items():
            measurement = xml.SubElement(measurements, "mon:Measurement")
            measurement_location = xml.SubElement(measurement, "loc:Location", ref=(index_key))
            value_units = xml.SubElement(measurement, "mon:Value", Unit="Sv/s").text = format(measurement_value, '.3g')
    measurements_tree = xml.ElementTree(measurement_root)
    return measurements_tree


def format_excel_data(excel_data):
    """This function changes structure of dict from
        data = {provider_key1: {index_key11: data11}, ..., {index_key12: data12},
                ...
                provider_keyN: {index_keyN1: dataN1, ..., {index_keyNN: dataNN}}
        }
        to dict
        data = {index_key11: data11, index_keyNN: dataNN}
    """

    pass


def get_nested_excel_element(excel_data, index_key):
    element = []
    for provider_key in excel_data:
        tmp = excel_data[provider_key].get(index_key)
        if tmp is not None:
            return tmp
    return None


def format_locations_subtree(measurement_data, excel_data):
    formatted_excel_data = format_excel_data(excel_data)
    locations_root = xml.Element("loc:Locations")
    for measurement_element in measurement_data:
        for index_key, tmp in measurement_element.items():
            excel_station = get_nested_excel_element(excel_data, index_key)
            location = xml.SubElement(locations_root, "loc:Location", id=(index_key))
            stantion_name = xml.SubElement(location, "loc:Name").text = excel_station.get('name_eng')
            geo_coord = xml.SubElement(location, "loc:GeographicCoordinates")
            latitude = xml.SubElement(geo_coord, "loc:Latitude").text = str(excel_station.get("latitude"))
            longitude = xml.SubElement(geo_coord, "loc:Longitude").text = str(excel_station.get(
                "longitude"))
            height = xml.SubElement(geo_coord, "loc:Height", Above="Sea", Unit="m").text = str(
                excel_station.get("altitude"))
    locations_tree = xml.ElementTree(locations_root)
    return locations_tree
