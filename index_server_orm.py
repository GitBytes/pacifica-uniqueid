"""
    ORM for index server
"""
import os
import peewee

# pylint: disable=too-few-public-methods

DB = peewee.MySQLDatabase(os.getenv('MYSQL_ENV_MYSQL_DATABASE', 'indexdb'),
                          host=os.getenv('MYSQL_PORT_3306_TCP_ADDR', '127.0.0.1'),
                          port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT', 3306)),
                          user=os.getenv('MYSQL_ENV_MYSQL_USER', 'root'),
                          passwd=os.getenv('MYSQL_ENV_MYSQL_PASSWORD', 'dummy'))

class UniqueIndex(peewee.Model):
    """
    auto-generated by pwiz
    maps a python record to a mysql table
    """
    idid = peewee.CharField(primary_key=True, db_column='id')
    index = peewee.BigIntegerField(db_column='index')


    class Meta(object):
        """
        map to the database connected above
        """
        database = DB
        only_save_dirty = True

    @classmethod
    def atomic(cls):
        """Get the atomic context or decorator"""
        # pylint: disable=no-member
        return cls._meta.database.atomic()
        # pylint: enable=no-member

    @classmethod
    def database_connect(cls):
        """Makes sure database is connected.  Trying to connect a second
        time doesnt cause any problems"""
        # pylint: disable=no-member
        cls._meta.database.connect()
        # pylint: enable=no-member

    @classmethod
    def database_close(cls):
        """Closes the database connection. Closing already closed database
        throws an error so catch it and continue on"""
        try:
            # pylint: disable=no-member
            cls._meta.database.close()
            # pylint: enable=no-member
        except peewee.ProgrammingError:
            #error for closing an already closed database so continue on
            return

def update_index(id_range, id_mode):
    """
    updates the index for a mode and returns a unique start and stop index
    """

    index = -1
    id_range = id_range

    try:
        with UniqueIndex.atomic():
            if id_range and id_mode and id_range > 0:
                record = UniqueIndex.get_or_create(idid=id_mode, defaults={'index':0})[0]
                index = int(record.index)
                record.index = index + id_range
                record.save()
            else:
                index = -1
                id_range = long(-1)
    except peewee.OperationalError:
        index = -1
        id_range = long(-1)

    return (index, id_range)
