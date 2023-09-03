import xml.etree.ElementTree as ET


class XmlTreeHelper:
    def add_tags_with_text(self, parent, tags):
        elements = []
        for tag in tags:
            element = ET.SubElement(parent, tag)
            element.text = tags[tag]
            elements.append(element)
        return elements


root = ET.Element('shop')

category = ET.SubElement(root, 'category', {'name': 'Vegan Products'})

product_1 = ET.SubElement(category, 'product', {'name': 'Good Morning Sunshine'})
product_2 = ET.SubElement(category, 'product', {'name': 'Spaghetti Veganietto'})
product_3 = ET.SubElement(category, 'product', {'name': 'Fantastic Almond Milk'})

xml_tree_helper = XmlTreeHelper()

xml_tree_helper.add_tags_with_text(product_1, {
    'type': 'cereals',
    'producer': 'OpenEDG Foods Limited',
    'price': '9.90',
    'currency': 'USD'
})

xml_tree_helper.add_tags_with_text(product_2, {
    'type': 'pasta',
    'producer': 'Programmers Eat Pasta Gmbh',
    'price': '14.49',
    'currency': 'EUR'
})

xml_tree_helper.add_tags_with_text(product_3, {
    'type': 'beverages',
    'producer': 'Drinks4Coders Inc.',
    'price': '19.75',
    'currency': 'USD'
})

# ET.dump(root)

tree = ET.ElementTree(root)
tree.write('resources/shop.xml', 'UTF-8', True)
