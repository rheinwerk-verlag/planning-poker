Development Setup
=================

If you want to help the development of this application and need a working setup, you can follow the steps below:

#. Clone the repository and move into the directory. ::

   $ git clone -b development https://github.com/rheinwerk-verlag/planning-poker.git
   $ cd planning-poker

#. Install the Python requirements. ::

   $ pip install -r requirements/dev.txt

#. Install the JavaScript requirements (you should at least use node version 10). ::

   $ npm install

#. Run the Django migrations. ::

   $ python manage.py migrate

#. Bundle the JS files. ::

   $ npm run build

   [Optional] If you plan to make changes to the Vue components or any other JS files during your development process,
   you should navigate to the project directory in a different terminal and run the webpack building process. This will
   automatically re-bundle your JS files whenever you make any changes to them. ::

   $ npm run build-dev

#. It is useful to have a superuser while developing. ::

   $ python manage.py createsuperuser

#. Finally, start your development server. ::

   $ python manage.py runserver 0.0.0.0:8000

.. note::

   There is an example project in this repository which has configured all the necessary settings for a minimal working
   setup. Feel free to configure the project to your liking while developing. See the
   :ref:`user_docs/configuration:Configuration` section for more ways you can configure this setup.

See the :ref:`dev_docs/testing:Testing` page and run the tests to verify that you have correctly set everything up.
