'''
This module provides support for defining relationships between your Elixir 
entities.  Elixir currently supports two syntaxes to do so: the default
`Attribute-based syntax`_ which supports the following types of relationships:
ManyToOne_, OneToMany_, OneToOne_ and ManyToMany_, as well as a 
`DSL-based syntax`_ which provides the following statements: belongs_to_, 
has_many_, has_one_ and has_and_belongs_to_many_. 

======================
Attribute-based syntax
======================

The first argument to all these "normal" relationship classes is the name of 
the class (entity) you are relating to. 

Following that first mandatory argument, any number of additional keyword 
arguments can be specified for advanced behavior. See each relationship type 
for a list of their specific keyword arguments. At this point, we'll just note
that all the arguments that are not specifically processed by Elixir, as 
mentioned in the documentation below are passed on to the SQLAlchemy 
``relation`` function. So, please refer to the `SQLAlchemy relation function's 
documentation <http://www.sqlalchemy.org/docs/04/sqlalchemy_orm.html
#docstrings_sqlalchemy.orm_modfunc_relation>`_ for further detail about which 
keyword arguments are supported. 

You should keep in mind that the following 
keyword arguments are automatically generated by Elixir and should not be used 
unless you want to override the value provided by Elixir: ``uselist``, 
``remote_side``, ``secondary``, ``primaryjoin`` and ``secondaryjoin``.

Additionally, if you want a bidirectionnal relationship, you should define the
inverse relationship on the other entity explicitly (as opposed to how
SQLAlchemy's backrefs are defined). In non-ambiguous situations, Elixir will 
match relationships together automatically. If there are several relationships
of the same type between two entities, Elixir is not able to determine which 
relationship is the inverse of which, so you have to disambiguate the 
situation by giving the name of the inverse relationship in the ``inverse`` 
keyword argument.

Here is a detailed explanation of each relation type:

`ManyToOne`
-----------

Describes the child's side of a parent-child relationship.  For example, 
a `Pet` object may belong to its owner, who is a `Person`.  This could be
expressed like so:

.. sourcecode:: python

    class Pet(Entity):
        owner = ManyToOne('Person')

Behind the scene, assuming the primary key of the `Person` entity is 
an integer column named `id`, the ``ManyToOne`` relationship will 
automatically add an integer column named `owner_id` to the entity, with a 
foreign key referencing the `id` column of the `Person` entity.

In addition to the keyword arguments inherited from SQLAlchemy's relation 
function, ``ManyToOne`` relationships accept the following optional arguments
which will be directed to the created column:

+----------------------+------------------------------------------------------+
| Option Name          | Description                                          |
+======================+======================================================+
| ``colname``          | Specify a custom column name.                        |
+----------------------+------------------------------------------------------+
| ``required``         | Specify whether or not this field can be set to None |
|                      | (left without a value). Defaults to ``False``,       |
|                      | unless the field is a primary key.                   |
+----------------------+------------------------------------------------------+
| ``primary_key``      | Specify whether or not the column(s) created by this |
|                      | relationship should act as a primary_key.            |
|                      | Defaults to ``False``.                               |
+----------------------+------------------------------------------------------+
| ``column_kwargs``    | A dictionary holding any other keyword argument you  |
|                      | might want to pass to the Column.                    |
+----------------------+------------------------------------------------------+

The following optional arguments are also supported to customize the
ForeignKeyConstraint that is created:

+----------------------+------------------------------------------------------+
| Option Name          | Description                                          |
+======================+======================================================+
| ``use_alter``        | If True, SQLAlchemy will add the constraint in a     |
|                      | second SQL statement (as opposed to within the       |
|                      | create table statement). This permits to define      |
|                      | tables with a circular foreign key dependency        |
|                      | between them.                                        |
+----------------------+------------------------------------------------------+
| ``ondelete``         | Value for the foreign key constraint ondelete clause.|
|                      | May be one of: ``cascade``, ``restrict``,            |
|                      | ``set null``, or ``set default``.                    |
+----------------------+------------------------------------------------------+
| ``onupdate``         | Value for the foreign key constraint onupdate clause.|
|                      | May be one of: ``cascade``, ``restrict``,            |
|                      | ``set null``, or ``set default``.                    |
+----------------------+------------------------------------------------------+
| ``constraint_kwargs``| A dictionary holding any other keyword argument you  |
|                      | might want to pass to the Constraint.                |
+----------------------+------------------------------------------------------+

Additionally, Elixir supports the belongs_to_ statement as an alternative, 
DSL-based, syntax to define ManyToOne_ relationships.


`OneToMany`
-----------

Describes the parent's side of a parent-child relationship when there can be
several children.  For example, a `Person` object has many children, each of
them being a `Person`. This could be expressed like so:

.. sourcecode:: python

    class Person(Entity):
        parent = ManyToOne('Person')
        children = OneToMany('Person')

Note that a ``OneToMany`` relationship **cannot exist** without a 
corresponding ``ManyToOne`` relationship in the other way. This is because the
``OneToMany`` relationship needs the foreign key created by the ``ManyToOne`` 
relationship.

In addition to keyword arguments inherited from SQLAlchemy, ``OneToMany`` 
relationships accept the following optional (keyword) arguments:

+--------------------+--------------------------------------------------------+
| Option Name        | Description                                            |
+====================+========================================================+
| ``order_by``       | Specify which field(s) should be used to sort the      |
|                    | results given by accessing the relation field. You can |
|                    | either use a string or a list of strings, each         |
|                    | corresponding to the name of a field in the target     |
|                    | entity. These field names can optionally be prefixed   |
|                    | by a minus (for descending order).                     |
+--------------------+--------------------------------------------------------+

Additionally, Elixir supports an alternate, DSL-based, syntax to define
OneToMany_ relationships, with the has_many_ statement.

Also, as for standard SQLAlchemy relations, the ``order_by`` keyword argument 


`OneToOne`
----------

Describes the parent's side of a parent-child relationship when there is only
one child.  For example, a `Car` object has one gear stick, which is 
represented as a `GearStick` object. This could be expressed like so:

.. sourcecode:: python

    class Car(Entity):
        gear_stick = OneToOne('GearStick', inverse='car')

    class GearStick(Entity):
        car = ManyToOne('Car')

Note that a ``OneToOne`` relationship **cannot exist** without a corresponding 
``ManyToOne`` relationship in the other way. This is because the ``OneToOne``
relationship needs the foreign_key created by the ``ManyToOne`` relationship.

Additionally, Elixir supports an alternate, DSL-based, syntax to define
OneToOne_ relationships, with the has_one_ statement.


`ManyToMany`
------------

Describes a relationship in which one kind of entity can be related to several
objects of the other kind but the objects of that other kind can be related to
several objects of the first kind.  For example, an `Article` can have several
tags, but the same `Tag` can be used on several articles.

.. sourcecode:: python

    class Article(Entity):
        tags = ManyToMany('Tag')

    class Tag(Entity):
        articles = ManyToMany('Article')

Behind the scene, the ``ManyToMany`` relationship will 
automatically create an intermediate table to host its data.

Note that you don't necessarily need to define the inverse relationship.  In
our example, even though we want tags to be usable on several articles, we 
might not be interested in which articles correspond to a particular tag.  In
that case, we could have omitted the `Tag` side of the relationship.

If the entity containing your ``ManyToMany`` relationship is 
autoloaded, you **must** specify at least one of either the ``remote_side`` or
``local_side`` argument.

In addition to keyword arguments inherited from SQLAlchemy, ``ManyToMany`` 
relationships accept the following optional (keyword) arguments:

+--------------------+--------------------------------------------------------+
| Option Name        | Description                                            |
+====================+========================================================+
| ``tablename``      | Specify a custom name for the intermediary table. This |
|                    | can be used both when the tables needs to be created   |
|                    | and when the table is autoloaded/reflected from the    |
|                    | database.                                              |
+--------------------+--------------------------------------------------------+
| ``remote_side``    | A column name or list of column names specifying       |
|                    | which column(s) in the intermediary table are used     |
|                    | for the "remote" part of a self-referential            |
|                    | relationship. This argument has an effect only when    |
|                    | your entities are autoloaded.                          |
+--------------------+--------------------------------------------------------+
| ``local_side``     | A column name or list of column names specifying       |
|                    | which column(s) in the intermediary table are used     |
|                    | for the "local" part of a self-referential             |
|                    | relationship. This argument has an effect only when    |
|                    | your entities are autoloaded.                          |
+--------------------+--------------------------------------------------------+
| ``order_by``       | Specify which field(s) should be used to sort the      |
|                    | results given by accessing the relation field. You can |
|                    | either use a string or a list of strings, each         |
|                    | corresponding to the name of a field in the target     |
|                    | entity. These field names can optionally be prefixed   |
|                    | by a minus (for descending order).                     |
+--------------------+--------------------------------------------------------+
| ``column_format``  | Specify an alternate format string for naming the      |
|                    | columns in the mapping table.  The default value is    |
|                    | defined in ``elixir.options.M2MCOL_NAMEFORMAT``.  You  |
|                    | will be passed ``tablename``, ``key``, and ``entity``  |
|                    | as arguments to the format string.                     |
+--------------------+--------------------------------------------------------+


================
DSL-based syntax
================

The following DSL statements provide an alternative way to define relationships
between your entities. The first argument to all those statements is the name 
of the relationship, the second is the 'kind' of object you are relating to 
(it is usually given using the ``of_kind`` keyword). 

`belongs_to`
------------

The ``belongs_to`` statement is the DSL syntax equivalent to the ManyToOne_
relationship. As such, it supports all the same arguments as ManyToOne_
relationships.

.. sourcecode:: python

    class Pet(Entity):
        belongs_to('feeder', of_kind='Person')
        belongs_to('owner', of_kind='Person', colname="owner_id")


`has_many`
----------

The ``has_many`` statement is the DSL syntax equivalent to the OneToMany_
relationship. As such, it supports all the same arguments as OneToMany_
relationships.

.. sourcecode:: python

    class Person(Entity):
        belongs_to('parent', of_kind='Person')
        has_many('children', of_kind='Person')

There is also an alternate form of the ``has_many`` relationship that takes 
only two keyword arguments: ``through`` and ``via`` in order to encourage a 
richer form of many-to-many relationship that is an alternative to the 
``has_and_belongs_to_many`` statement.  Here is an example:

.. sourcecode:: python

    class Person(Entity):
        has_field('name', Unicode)
        has_many('assignments', of_kind='Assignment')
        has_many('projects', through='assignments', via='project')

    class Assignment(Entity):
        has_field('start_date', DateTime)
        belongs_to('person', of_kind='Person')
        belongs_to('project', of_kind='Project')

    class Project(Entity):
        has_field('title', Unicode)
        has_many('assignments', of_kind='Assignment')

In the above example, a `Person` has many `projects` through the `Assignment`
relationship object, via a `project` attribute.


`has_one`
---------

The ``has_one`` statement is the DSL syntax equivalent to the OneToOne_
relationship. As such, it supports all the same arguments as OneToOne_
relationships.

.. sourcecode:: python

    class Car(Entity):
        has_one('gear_stick', of_kind='GearStick', inverse='car')

    class GearStick(Entity):
        belongs_to('car', of_kind='Car')


`has_and_belongs_to_many`
-------------------------

The ``has_and_belongs_to_many`` statement is the DSL syntax equivalent to the 
ManyToMany_ relationship. As such, it supports all the same arguments as
ManyToMany_ relationships.

.. sourcecode:: python

    class Article(Entity):
        has_and_belongs_to_many('tags', of_kind='Tag')

    class Tag(Entity):
        has_and_belongs_to_many('articles', of_kind='Article')

'''

from sqlalchemy         import ForeignKeyConstraint, Column, \
                               Table, and_
from sqlalchemy.orm     import relation, backref
from elixir.statements  import ClassMutator
from elixir.fields      import Field
from elixir.properties  import Property
from elixir.entity      import EntityDescriptor, EntityMeta
from sqlalchemy.ext.associationproxy import association_proxy

from py23compat import rsplit

import sys
import options

__doc_all__ = []

class Relationship(Property):
    '''
    Base class for relationships.
    '''
    
    def __init__(self, of_kind, *args, **kwargs):
        super(Relationship, self).__init__()

        self.inverse_name = kwargs.pop('inverse', None)

        self.of_kind = of_kind

        self._target = None
        self._inverse = None
        
        self.property = None # sqlalchemy property
        self.backref = None  # sqlalchemy backref

        #TODO: unused for now
        self.args = args
        self.kwargs = kwargs

    def attach(self, entity, name):
        super(Relationship, self).attach(entity, name)
        entity._descriptor.relationships.append(self)
    
    def create_pk_cols(self):
        self.create_keys(True)

    def create_non_pk_cols(self):
        self.create_keys(False)

    def create_keys(self, pk):
        '''
        Subclasses (ie. concrete relationships) may override this method to 
        create foreign keys.
        '''
    
    def create_tables(self):
        '''
        Subclasses (ie. concrete relationships) may override this method to 
        create secondary tables.
        '''
    
    def create_properties(self):
        '''
        Subclasses (ie. concrete relationships) may override this method to
        add properties to the involved entities.
        '''
        if self.property or self.backref:
            return

        kwargs = {}
        if self.inverse:
            # check if the inverse was already processed (and thus has already
            # defined a backref we can use)
            if self.inverse.backref:
                kwargs['backref'] = self.inverse.backref
            else:
                kwargs = self.get_prop_kwargs()

                # SQLAlchemy doesn't like when 'secondary' is both defined on
                # the relation and the backref
                kwargs.pop('secondary', None)

                # define backref for use by the inverse
                self.backref = backref(self.name, **kwargs)
                return

        kwargs.update(self.get_prop_kwargs())
        self.property = relation(self.target, **kwargs)
        self.entity._descriptor.add_property(self.name, self.property)
    
    def target(self):
        if not self._target:
            if isinstance(self.of_kind, EntityMeta):
                self._target = self.of_kind
            else:
                path = rsplit(self.of_kind, '.', 1)
                classname = path.pop()

                if path:
                    # do we have a fully qualified entity name?
                    module = sys.modules[path.pop()]
                    self._target = getattr(module, classname, None)
                else:
                    # If not, try the list of entities of the "caller" of the 
                    # source class. Most of the time, this will be the module 
                    # the class is defined in. But it could also be a method 
                    # (inner classes).
                    caller_entities = EntityMeta._entities[self.entity._caller]
                    self._target = caller_entities[classname]
        return self._target
    target = property(target)
    
    def inverse(self):
        if not self._inverse:
            if self.inverse_name:
                desc = self.target._descriptor
                inverse = desc.find_relationship(self.inverse_name)
                if inverse is None:
                    raise Exception(
                              "Couldn't find a relationship named '%s' in "
                              "entity '%s' or its parent entities." 
                              % (self.inverse_name, self.target.__name__))
                assert self.match_type_of(inverse)
            else:
                inverse = self.target._descriptor.get_inverse_relation(self)

            if inverse:
                self._inverse = inverse
                inverse._inverse = self
        
        return self._inverse
    inverse = property(inverse)
    
    def match_type_of(self, other):
        return False

    def is_inverse(self, other):
        return other is not self and \
               self.match_type_of(other) and \
               self.entity == other.target and \
               other.entity == self.target and \
               (self.inverse_name == other.name or not self.inverse_name) and \
               (other.inverse_name == self.name or not other.inverse_name)


class ManyToOne(Relationship):
    '''
    
    '''
    
    def __init__(self, *args, **kwargs):
        self.colname = kwargs.pop('colname', [])
        if self.colname and not isinstance(self.colname, list):
            self.colname = [self.colname]

        self.column_kwargs = kwargs.pop('column_kwargs', {})
        if 'required' in kwargs:
            self.column_kwargs['nullable'] = not kwargs.pop('required')
        if 'primary_key' in kwargs:
            self.column_kwargs['primary_key'] = kwargs.pop('primary_key')
        # by default, columns created will have an index.
        self.column_kwargs.setdefault('index', True)

        self.constraint_kwargs = kwargs.pop('constraint_kwargs', {})
        if 'use_alter' in kwargs:
            self.constraint_kwargs['use_alter'] = kwargs.pop('use_alter')
        
        if 'ondelete' in kwargs:
            self.constraint_kwargs['ondelete'] = kwargs.pop('ondelete')
        if 'onupdate' in kwargs:
            self.constraint_kwargs['onupdate'] = kwargs.pop('onupdate')
        
        self.foreign_key = list()
        self.primaryjoin_clauses = list()

        super(ManyToOne, self).__init__(*args, **kwargs)
    
    def match_type_of(self, other):
        return isinstance(other, (OneToMany, OneToOne))

    def create_keys(self, pk):
        '''
        Find all primary keys on the target and create foreign keys on the 
        source accordingly.
        '''

        if self.foreign_key:
            return

        if self.column_kwargs.get('primary_key', False) != pk:
            return

        source_desc = self.entity._descriptor
        #TODO: make this work if target is a pure SA-mapped class
        # for that, I need: 
        # - the list of primary key columns of the target table (type and name)
        # - the name of the target table
        target_desc = self.target._descriptor
        #make sure the target has all its pk setup up
        target_desc.create_pk_cols()

        if source_desc.autoload:
            #TODO: test if this works when colname is a list

            if self.colname:
                self.primaryjoin_clauses = \
                    _get_join_clauses(self.entity.table, 
                                      self.colname, None, 
                                      self.target.table)[0]
                if not self.primaryjoin_clauses:
                    raise Exception(
                        "Couldn't find a foreign key constraint in table "
                        "'%s' using the following columns: %s."
                        % (self.entity.table.name, ', '.join(self.colname)))
        else:
            fk_refcols = list()
            fk_colnames = list()

            if self.colname and \
               len(self.colname) != len(target_desc.primary_keys):
                raise Exception(
                        "The number of column names provided in the colname "
                        "keyword argument of the '%s' relationship of the "
                        "'%s' entity is not the same as the number of columns "
                        "of the primary key of '%s'."
                        % (self.name, self.entity.__name__, 
                           self.target.__name__))

            pks = target_desc.primary_keys
            if not pks:
                raise Exception("No primary key found in target table ('%s') "
                                "for the '%s' relationship of the '%s' entity."
                                % (self.target.tablename, self.name, 
                                   self.entity.__name__))

            for key_num, pk_col in enumerate(pks):
                if self.colname:
                    colname = self.colname[key_num]
                else:
                    colname = options.FKCOL_NAMEFORMAT % \
                              {'relname': self.name, 
                               'key': pk_col.key}

                # We can't add the column to the table directly as the table
                # might not be created yet.
                col = Column(colname, pk_col.type, **self.column_kwargs)
                source_desc.add_column(col)

                # Build the list of local columns which will be part of
                # the foreign key
                self.foreign_key.append(col)

                # Store the names of those columns
                fk_colnames.append(col.key)

                # Build the list of column "paths" the foreign key will 
                # point to
                target_path = "%s.%s" % (target_desc.tablename, pk_col.key)
                schema = target_desc.table_options.get('schema', None)
                if schema is not None:
                    target_path = "%s.%s" % (schema, target_path)
                fk_refcols.append(target_path)

                # Build up the primary join. This is needed when you have 
                # several belongs_to relationships between two objects
                self.primaryjoin_clauses.append(col == pk_col)
            
            if 'name' not in self.constraint_kwargs:
                # In some databases (at least MySQL) the constraint name needs
                # to be unique for the whole database, instead of per table.
                fk_name = options.CONSTRAINT_NAMEFORMAT % \
                          {'tablename': source_desc.tablename, 
                           'colnames': '_'.join(fk_colnames)}
                self.constraint_kwargs['name'] = fk_name
                
            source_desc.add_constraint(
                ForeignKeyConstraint(fk_colnames, fk_refcols,
                                     **self.constraint_kwargs))

    def get_prop_kwargs(self):
        kwargs = {'uselist': False}
        
        if self.entity.table is self.target.table:
            kwargs['remote_side'] = \
                [col for col in self.target.table.primary_key.columns]

        if self.primaryjoin_clauses:
            kwargs['primaryjoin'] = and_(*self.primaryjoin_clauses)

        kwargs.update(self.kwargs)

        return kwargs


class OneToOne(Relationship):
    uselist = False

    def match_type_of(self, other):
        return isinstance(other, ManyToOne)

    def create_keys(self, pk):
        # make sure an inverse relationship exists
        if self.inverse is None:
            raise Exception(
                      "Couldn't find any relationship in '%s' which "
                      "match as inverse of the '%s' relationship "
                      "defined in the '%s' entity. If you are using "
                      "inheritance you "
                      "might need to specify inverse relationships "
                      "manually by using the inverse keyword."
                      % (self.target.__name__, self.name,
                         self.entity.__name__))
    
    def get_prop_kwargs(self):
        kwargs = {'uselist': self.uselist}
        
        #TODO: for now, we don't break any test if we remove those 2 lines.
        # So, we should either complete the selfref test to prove that they
        # are indeed useful, or remove them. It might be they are indeed
        # useless because of the primaryjoin, and that the remote_side is
        # already setup in the other way (belongs_to).
        if self.entity.table is self.target.table:
            #FIXME: IF this code is of any use, it will probably break for
            # autoloaded tables
            kwargs['remote_side'] = self.inverse.foreign_key
        
        if self.inverse.primaryjoin_clauses:
            kwargs['primaryjoin'] = and_(*self.inverse.primaryjoin_clauses)

        kwargs.update(self.kwargs)

        return kwargs


class OneToMany(OneToOne):
    uselist = True
    
    def get_prop_kwargs(self):
        kwargs = super(OneToMany, self).get_prop_kwargs()

        if 'order_by' in kwargs:
            kwargs['order_by'] = \
                self.target._descriptor.translate_order_by(
                    kwargs['order_by'])

        return kwargs


class ManyToMany(Relationship):
    uselist = True

    def __init__(self, *args, **kwargs):
        self.user_tablename = kwargs.pop('tablename', None)
        self.local_side = kwargs.pop('local_side', [])
        if self.local_side and not isinstance(self.local_side, list):
            self.local_side = [self.local_side]
        self.remote_side = kwargs.pop('remote_side', [])
        if self.remote_side and not isinstance(self.remote_side, list):
            self.remote_side = [self.remote_side]
        self.ondelete = kwargs.pop('ondelete', None)
        self.onupdate = kwargs.pop('onupdate', None)
        self.column_format = kwargs.pop('column_format', options.M2MCOL_NAMEFORMAT)

        self.secondary_table = None
        self.primaryjoin_clauses = list()
        self.secondaryjoin_clauses = list()

        super(ManyToMany, self).__init__(*args, **kwargs)

    def match_type_of(self, other):
        return isinstance(other, ManyToMany)

    def create_tables(self):
        if self.secondary_table:
            return
        
        if self.inverse:
            if self.inverse.secondary_table:
                self.secondary_table = self.inverse.secondary_table
                self.primaryjoin_clauses = self.inverse.secondaryjoin_clauses
                self.secondaryjoin_clauses = self.inverse.primaryjoin_clauses
                return

        e1_desc = self.entity._descriptor
        e2_desc = self.target._descriptor
       
        # First, we compute the name of the table. Note that some of the 
        # intermediary variables are reused later for the constraint 
        # names.
        
        # We use the name of the relation for the first entity 
        # (instead of the name of its primary key), so that we can 
        # have two many-to-many relations between the same objects 
        # without having a table name collision. 
        source_part = "%s_%s" % (e1_desc.tablename, self.name)

        # And we use only the name of the table of the second entity
        # when there is no inverse, so that a many-to-many relation 
        # can be defined without an inverse.
        if self.inverse:
            target_part = "%s_%s" % (e2_desc.tablename, self.inverse.name)
        else:
            target_part = e2_desc.tablename
        
        if self.user_tablename:
            tablename = self.user_tablename
        else:
            # We need to keep the table name consistent (independant of 
            # whether this relation or its inverse is setup first).
            if self.inverse and e1_desc.tablename < e2_desc.tablename:
                tablename = "%s__%s" % (target_part, source_part)
            else:
                tablename = "%s__%s" % (source_part, target_part)

        if e1_desc.autoload:
            self._reflect_table(tablename)
        else:
            # We pre-compute the names of the foreign key constraints 
            # pointing to the source (local) entity's table and to the 
            # target's table

            # In some databases (at least MySQL) the constraint names need 
            # to be unique for the whole database, instead of per table.
            source_fk_name = "%s_fk" % source_part
            if self.inverse:
                target_fk_name = "%s_fk" % target_part
            else:
                target_fk_name = "%s_inverse_fk" % source_part

            columns = list()
            constraints = list()

            joins = (self.primaryjoin_clauses, self.secondaryjoin_clauses)
            for num, desc, fk_name, m2m in (
                    (0, e1_desc, source_fk_name, self), 
                    (1, e2_desc, target_fk_name, self.inverse)):
                fk_colnames = list()
                fk_refcols = list()
            
                for pk_col in desc.primary_keys:
                    colname = self.column_format % \
                              {'tablename': desc.tablename,
                               'key': pk_col.key,
                               'entity': desc.entity.__name__.lower()}
                    
                    # In case we have a many-to-many self-reference, we 
                    # need to tweak the names of the columns so that we 
                    # don't end up with twice the same column name.
                    if self.entity is self.target:
                        colname += str(num + 1)
                    
                    col = Column(colname, pk_col.type, primary_key=True)
                    columns.append(col)

                    # Build the list of local columns which will be part 
                    # of the foreign key.
                    fk_colnames.append(colname)

                    # Build the list of columns the foreign key will point
                    # to.
                    fk_refcols.append(desc.tablename + '.' + pk_col.key)

                    # Build join clauses (in case we have a self-ref)
                    if self.entity is self.target:
                        joins[num].append(col == pk_col)
                
                onupdate = m2m and m2m.onupdate
                ondelete = m2m and m2m.ondelete
                
                constraints.append(
                    ForeignKeyConstraint(fk_colnames, fk_refcols,
                                         name=fk_name, onupdate=onupdate, 
                                         ondelete=ondelete))

            args = columns + constraints
            
            self.secondary_table = Table(tablename, e1_desc.metadata, 
                                         *args)

    def _reflect_table(self, tablename):
        if not self.target._descriptor.autoload:
            raise Exception(
                "Entity '%s' is autoloaded and its '%s' "
                "has_and_belongs_to_many relationship points to "
                "the '%s' entity which is not autoloaded"
                % (self.entity.__name__, self.name,
                   self.target.__name__))
                
        self.secondary_table = Table(tablename, 
                                     self.entity._descriptor.metadata,
                                     autoload=True)

        # In the case we have a self-reference, we need to build join clauses
        if self.entity is self.target:
            #CHECKME: maybe we should try even harder by checking if that 
            # information was defined on the inverse relationship)
            if not self.local_side and not self.remote_side:
                raise Exception(
                    "Self-referential has_and_belongs_to_many "
                    "relationships in autoloaded entities need to have at "
                    "least one of either 'local_side' or 'remote_side' "
                    "argument specified. The '%s' relationship in the '%s' "
                    "entity doesn't have either."
                    % (self.name, self.entity.__name__))

            self.primaryjoin_clauses, self.secondaryjoin_clauses = \
                _get_join_clauses(self.secondary_table, 
                                  self.local_side, self.remote_side, 
                                  self.entity.table)

    def get_prop_kwargs(self):
        kwargs = {'secondary': self.secondary_table, 
                  'uselist': self.uselist}

        if self.target is self.entity:
            kwargs['primaryjoin'] = and_(*self.primaryjoin_clauses)
            kwargs['secondaryjoin'] = and_(*self.secondaryjoin_clauses)

        kwargs.update(self.kwargs)

        if 'order_by' in kwargs:
            kwargs['order_by'] = \
                self.target._descriptor.translate_order_by(kwargs['order_by'])

        return kwargs

    def is_inverse(self, other):
        return super(ManyToMany, self).is_inverse(other) and \
               (self.user_tablename == other.user_tablename or 
                (not self.user_tablename and not other.user_tablename))


def _get_join_clauses(local_table, local_cols1, local_cols2, target_table):
    primary_join, secondary_join = [], []
    cols1 = local_cols1[:]
    cols1.sort()
    cols1 = tuple(cols1)

    if local_cols2 is not None:
        cols2 = local_cols2[:]
        cols2.sort()
        cols2 = tuple(cols2)
    else:
        cols2 = None

    # Build a map of fk constraints pointing to the correct table.
    # The map is indexed on the local col names.
    constraint_map = {}
    for constraint in local_table.constraints:
        if isinstance(constraint, ForeignKeyConstraint):

            use_constraint = True
            fk_colnames = []

            # if all columns point to the correct table, we use the constraint
            for fk in constraint.elements:
                if fk.references(target_table):
                    fk_colnames.append(fk.parent.key)
                else:
                    use_constraint = False
            if use_constraint:
                fk_colnames.sort()
                constraint_map[tuple(fk_colnames)] = constraint

    # Either the fk column names match explicitely with the columns given for
    # one of the joins (primary or secondary), or we assume the current
    # columns match because the columns for this join were not given and we
    # know the other join is either not used (is None) or has an explicit 
    # match.
        
#TODO: rewrite this. Even with the comment, I don't even understand it myself.
    for cols, constraint in constraint_map.iteritems():
        if cols == cols1 or (cols != cols2 and 
                             not cols1 and (cols2 in constraint_map or
                                            cols2 is None)):
            join = primary_join
        elif cols == cols2 or (cols2 == () and cols1 in constraint_map):
            join = secondary_join
        else:
            continue
        for fk in constraint.elements:
            join.append(fk.parent == fk.column)
    return primary_join, secondary_join


def rel_mutator_handler(target):
    def handler(entity, name, *args, **kwargs):
        if 'through' in kwargs and 'via' in kwargs:
            setattr(entity, name, 
                    association_proxy(kwargs.pop('through'), 
                                      kwargs.pop('via'),
                                      **kwargs))
            return
        elif 'through' in kwargs or 'via' in kwargs:
            raise Exception("'through' and 'via' relationship keyword "
                            "arguments should be used in combination.")
        rel = target(kwargs.pop('of_kind'), *args, **kwargs)
        rel.attach(entity, name)
    return handler


belongs_to = ClassMutator(rel_mutator_handler(ManyToOne))
has_one = ClassMutator(rel_mutator_handler(OneToOne))
has_many = ClassMutator(rel_mutator_handler(OneToMany))
has_and_belongs_to_many = ClassMutator(rel_mutator_handler(ManyToMany))
