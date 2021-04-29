from settings import db


class BaseMixin(object):
    @classmethod
    def create(cls, **kw):
        """
        This function inserts a new row into the table and returns the row that has been added.
        """

        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()

        return obj
