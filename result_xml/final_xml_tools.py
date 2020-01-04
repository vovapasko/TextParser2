import uuid
import xml.etree.ElementTree as xml
from datetime import datetime

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
    return first


def format_identification_subtree(file):
    file_data = xml.parse(file)

    id_root = xml.Element("id:Identification")
    org_reporting = xml.SubElement(id_root, "id:OrganisationReporting").text = file_data.find(
        "OrganisationReporting").text
    time = datetime.now()
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
