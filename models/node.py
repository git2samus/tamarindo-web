from google.appengine.ext import db


class Node(db.Model):
    title = db.StringProperty()
    associations = db.ListProperty(db.Key)

    @property
    def quoted_title(self):
        return "\"%s\"" % self.title.replace("\\", "\\\\").replace("\"", "\\\"")

    def digraph(self, nodes_dict=None):
        if self.associations:
            nodes_dict = nodes_dict or dict((node.key(), node) for node in Node.get(self.associations))
            return ','.join("%s->%s" % (self.quoted_title, nodes_dict[child_key].quoted_title) for child_key in self.associations)
        else:
            return self.quoted_title

