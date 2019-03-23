from selenium import webdriver
from lxml import etree, html

class codeBeautifier:
    def __init__(self):
        self.HTML_Code = ""
        self.CSS_Code = ""
        self.Javascript_Code = ""

    def prettyHTML(self, HTMLString):
        self.HTML_Code = HTMLString
        document_root = html.fromstring(self.HTML_Code)
        return etree.tostring(document_root, encoding='unicode', pretty_print=True)

    def prettyCSS(self, CSSString):
        self.CSS_Code = CSSString
        document_root = html.fromstring(self.CSS_Code)
        return etree.tostring(document_root, encoding='unicode', pretty_print=True)


tempHTML = """<!DOCTYPE html><html lang="en"><head><title>Generated Site</title><meta charset="UTF-8"><link 
rel="stylesheet" href="layout.css" type="text/css"></head><body><div class="wrapper row1"><header id="header" 
class="clear"><div id="hgroup"><h1><a href="#">Generated Website</a></h1><h2>Your Motto Goes 
Here</h2></div><nav><ul><li class="last"><a href="#">Text Link</a></li></ul></nav></header></div><div class="wrapper 
row2"><div id="container" class="clear"><section id="imgLTxtR" class="clear"><figure><img src="Blank-grey.gif" 
alt=""><figcaption><h2>Nunc nec est diam.</h2><p>Fusce laoreet pellentesque lectus in blandit. Morbi efficitur 
blandit metus, eu convallis nunc venenatis eu. Praesent enim arcu, volutpat id elit eu, hendrerit aliquam odio. 
Aenean posuere nibh erat, vel condimentum turpis condimentum quis. Praesent elit tellus, interdum eget ornare 
commodo, rhoncus quis nibh. </p></figcaption></figure></section><section id="imgLTxtR" class="clear"><figure><img 
src="Blank-grey.gif" alt=""><figcaption><h2>Fusce at auctor lorem.</h2><p>Integer auctor sapien ac varius gravida. 
Vivamus justo elit, luctus id sollicitudin et, semper ut mauris. Maecenas eget lorem dignissim, ultrices leo 
pellentesque, vehicula tortor. Maecenas eget lorem dignissim, ultrices leo pellentesque, vehicula tortor. Fusce at 
auctor lorem. Mauris et rutrum felis. </p></figcaption></figure></section><section id="imgTTxtB" 
class="clear"><figure><img src="Blank-grey.gif" alt=""><figcaption><h2>Nunc nec est diam.</h2><p>Fusce faucibus metus 
sed dui posuere suscipit. Etiam iaculis a mi quis efficitur. Aliquam sit amet ante arcu. Pellentesque facilisis justo 
eu diam consequat suscipit. Duis placerat metus ex, ut porta dolor pharetra non. Pellentesque convallis posuere odio, 
at sollicitudin mauris blandit eget. Nunc nec est diam. </p></figcaption></figure></section><section id="slider"><a 
href="#"><img src="Blank-grey.gif" alt="" style="width: 960px; height: 
360px;"></a></section></div></div></body></html> """

css = "div { white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}"

# print(codeBeautifier().prettyHTML(tempHTML))
# print(codeBeautifier().prettyCSS(css))
#
# with open('/Users/edwardlai/Documents/2019 Spring Assignments/HTML_Forge/App/temp.txt', 'w') as the_file:
#     the_file.write(codeBeautifier().prettyHTML(tempHTML))
# the_file.close()
