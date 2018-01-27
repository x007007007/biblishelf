Database Schema
===============

.. graphviz::

   digraph foo {
      "bar" -> "baz";
   }


.. graph:: foo

   "bar" -- "baz";

.. graphviz::

     digraph example {
         a [label="sphinx", href="http://sphinx-doc.org", target="_top"];
         b [label="other"];
         a -> b;
     }
