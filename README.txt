JS Content UX
=============

Add-on that adds support for tabbed and accordion view.

Both the sections can be placed within each other or can be used multiple times.

Tabbed section
--------------

The tabbed part is implemented using EasyTabs - http://os.alfajango.com/easytabs/

The expected html markup is::

    <div class="uol-tabs">
    <div class="uol-tabs-head">
        <ul>
        <li><a href="#sec-1">Section 1</a></li>
        <li><a href="#sec-2">Section 2</a></li>
        </ul>
    </div>

    <div class="uol-tabs-body">
        <div id="sec-1">
            ...
        </div>
    </div>

    <div class="uol-tabs-body">
        <div id="sec-2">
            ...
        </div>
    </div>
    </div>


Accordion section
-----------------

The accordion part is implemented using Plone's jQuery.

The expected html markup is::

    <div class="uol-accordion">
    <a class="show-all" href="#show-all">Show/Hide All</a>

    <div class="uol-accordion-section" id="sec-a">
        <div class="uol-accordion-head">
        <a href="#sec-a">Section A</a>
        </div>

        <div class="uol-accordion-body">
        ...
        </div>
    </div>

    <div class="uol-accordion-section" id="sec-b">
        <div class="uol-accordion-head">
        <a href="#sec-b">Section B</a>
        </div>

        <div class="uol-accordion-body">
        ...
        </div>
    </div>
    </div>


Site section limit
------------------

To limit the above to a different section of a site there is a control panel
called "Allowed sections settings". A list of absolute urls (without hostname) can
be provided to define at which section the javascript should be loaded.

It does not prevent anybody from adding this specific markup anywhere in the site.
