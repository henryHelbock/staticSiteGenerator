class HtmlNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        propsValuesCombined = ""
        for key,value in self.props.items():
            propsValuesCombined += (f" {key}={value}")
        
        return propsValuesCombined
    
    def __repr__(self):
        return(f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})")


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return (f"LeafNode({self.tag}, {self.value}, {self.props})")
