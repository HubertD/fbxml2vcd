import vobject
import xml.etree.ElementTree as ET


def add_name(vcard, full_name):
    fn = vcard.add('fn')
    fn.value = full_name
    parts = full_name.split()
    n = vcard.add('n')
    if len(parts) == 1:
        n.value = vobject.vcard.Name(family=parts[0])
    else:
        n.value = vobject.vcard.Name(given=parts[0], family=" ".join(parts[1:]))


def format_phone(number):
    if number.startswith("00"):
        return "+" + number[2:]
    elif number.startswith("0"):
        return "+49" + number[1:]
    else:
        return number


def add_phone(vcard, number, type):
    if number is not None:
        tel = vcard.add('tel')
        tel.type_param = type
        tel.value = format_phone(number)


xml = ET.parse("test.xml")
for contact in xml.iter("contact"):
    full_name = contact.findtext("./person/realName")
    vcard = vobject.vCard()
    add_name(vcard, full_name)
    for t in ('home', 'work', 'mobile'):
        add_phone(vcard, contact.findtext("./telephony/number[@type='%s']" % t), t)

    with open(full_name+".vcd", "w") as f:
        f.write(vcard.serialize())
