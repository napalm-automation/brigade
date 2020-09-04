Changelog
==========

2.5.0 - September 4 2020
------------------------

*  migrate to github actions :issue:`491` :user:`dbarrosop`
*  Delete /tmp/hosts before running gitlab plugin notebook cell :issue:`500` :user:`dmfigol`
*  Do not store failed connections in host attributes :issue:`497` :user:`dmfigol`
*  Improved whitespace handling in jinja template rendering :issue:`528` :user:`indy-independence`
*  pass ssh_config only if file exists :issue:`538` :user:`dbarrosop`
*  Allow nornir 2.x to use NAPALM 3.x without warnings :issue:`545` :user:`ktbyers`
*  Remove None default for source of napalm_ping :issue:`556` :user:`ThreeFDDI`
*  Update processors.ipynb :issue:`566` :user:`pablopenton`
*  NBInventory - adds device name if no primary IP :issue:`534` :user:`jvanderaa`
*  Adding license meta information to pyproject.toml :issue:`581` :user:`ktbyers`
*  fix netconf tests to accommodate latest container :issue:`582` :user:`dbarrosop`

2.4.0 - February 15 2020
------------------------

* vendor pydantic :issue:`482` :user:`dbarrosop`
* Netconf connection plugin does not respect ssh config :issue:`481` :user:`fach`
* Added napalm_ping.py plugin :issue:`472` :user:`tejasmokashi1992`
* Add skip mark to netconf tests :issue:`469` :user:`dmfigol`
* Update dependencies :issue:`468` :user:`dmfigol`
* Replace multiprocessing.dummy with concurrent.futures :issue:`467` :user:`dmfigol`
* Ansible Inventory - NornirNoValidInventoryError Exception :issue:`463` :user:`carlmontanari`
* cleanup items from :issue:`459` #462 :user:`carlmontanari`
* Update pydantic to v1 :issue:`449` :user:`AchilleAsh`
* Minor Typing updates to appease mypy .740 :issue:`448` :user:`carlmontanari`
* Update to support Netmiko 3.x.x :issue:`445` :user:`carlmontanari`
* Add netconf plugins :issue:`444` :user:`ogenstad`
* Fix KeyError when setting a "False" val in defaults :issue:`443` :user:`k01ek`
* Fix :issue:`411` #442 :user:`k01ek`
* Add Netbox inventory plugin to documentation :issue:`441` :user:`ogenstad`
* Add netconf_capabilities plugin :issue:`439` :user:`ogenstad`
* Fix netbox unnamed devices :issue:`438` :user:`wvandeun`

2.3.0 - September 21 2019
-------------------------

* Fixes (#406) ssl_verify in netbox plugin should accept string :issue:`434` by :user:`wvandeun`
* Add connection test for Netconf :issue:`427` by :user:`ogenstad`
* Fix Poetry link in .travis.yml: Install Poetry from official link :issue:`425` by :user:`ogenstad`
* Processors :issue:`424` by :user:`dbarrosop`
* Gitlab plugin: Fix global dry_run check :issue:`421` by :user:`ogenstad`
* Add tests for Host data functions :issue:`420` by :user:`ogenstad`
* Enable mypy for nornir.core.task :issue:`418` by :user:`ogenstad`
* NETCONF prototype :issue:`416` by :user:`dbarrosop`
* Add netmiko_commit task :issue:`414` by :user:`jrokeach`
* Allow the use of ~ in simple inventory file paths :issue:`408` by :user:`ktbyers`
* Minor docfix for failed hosts content :issue:`403` by :user:`ktbyers`
* added empty line so the docstring is properly formatted :issue:`399` by :user:`dbarrosop`
* added discourse link :issue:`398` by :user:`dbarrosop`
* add logo :issue:`395` by :user:`dbarrosop`
* Fix Nornir dict method and dependencies :issue:`394` by :user:`brandomando`
* Fix netbox pagination :issue:`392` by :user:`wvandeun`
* spelling fixes :issue:`389` by :user:`ka7`
* Fix markup for links to external resources :issue:`388` by :user:`vincentbernat`
* Fix add_host and add_group methods to re-initialize inventory :issue:`384` by :user:`brandomando`
* fix changelog format again :issue:`382` by :user:`dbarrosop`
* added howto "Adding a progress bar to nornir" :issue:`381` by :user:`dbarrosop`

2.2.0 - April 27 2019
---------------------

* [PLUGIN_NEW] Add gitlab file plugin :issue:`324`
* [DOCS] Fixed copyright in the LICENSE :issue:`378`
* [DOCS] added ipdb examples :issue:`376`
* [CORE_ENHANCEMENTS] Added functions to retrieve inventory using native datastructures :issue:`375`
* [DOCS] Added external resources :issue:`374`
* [MISC] Improve build
* [CORE_ENHANCEMENTS] Added add_host and add_group functions to nornir.core.inventory.Inventory class :issue:`372`
* [DOCS] Updating howto documentation for including 'ConnectionOptions' :issue:`365`
* [DOCS] Fixed typos :issue:`362` :issue:`360`

Thanks to the following people for their contributions:

* :user:`wvandeun`
* :user:`brandomando`
* :user:`dbarrosop`
* :user:`dmfigol`
* :user:`bdlamprecht`
* :user:`eakman`

2.1.1 - March 19 2019
---------------------

* [MISC] Workaround to sdispater/poetry:issue:`743` :issue:`358`
* [MISC] Fix automated deployment to pypi :issue:`358`

Thanks to the following people for their contributions:

* :user:`dbarrosop`

2.1.0 - March 18 2019
---------------------

* [CORE_ENHANCEMENTS] inventory's transform function supports options :issue:`292`
* [CORE_ENHANCEMENTS] minor improvements to tests :issue:`293` :issue:`296` :issue:`306` :issue:`307` :issue:`312` :issue:`337`
* [CORE_ENHANCEMENTS] mypy improvements :issue:`308`
* [CORE_ENHANCEMENTS] expand user home when deserializing configuration :issue:`304`
* [CORE_ENHANCEMENTS] fix order of preference when deserializing config :issue:`309`
* [CORE_ENHANCEMENTS] fix and deprecate dict() function :issue:`314`
* [CORE_ENHANCEMENTS] migrate to poetry :issue:`315`
* [CORE_ENHANCEMENTS] Improve logging :issue:`316`
* [CORE_BUGFIX] (windows only) fix issue :issue:`319` - ascii color codes appear instead of color in output :issue:`320` :issue:`323`
* [PLUGIN_IMPROVEMENT] napalm and netmiko plugins support now reading ssh configuration from file :issue:`298`
* [PLUGIN_BUGFIX] fix paramiko chan.recv_exit_status() call order :issue:`313`
* [PLUGIN_BUGFIX] temporary fix for enum34 and netmiko-poetry issue :issue:`322`
* [PLUGIN_IMPROVEMENT] Print OrderDicts nicely in print_result :issue:`345`
* [DOCS] Various improvements :issue:`303` :issue:`305` :issue:`310` :issue:`318` :issue:`331` :issue:`335` :issue:`340`

Thanks to the following people for their contributions:

* :user:`bradh11`
* :user:`fallenarc`
* :user:`floatingstatic`
* :user:`jimmelville`
* :user:`optiz0r`
* :user:`wdesmedt`
* :user:`dmfigol`
* :user:`ktbyers`
* :user:`dbarrosop`

2.0.0 - December 17 2018
------------------------

For details about upgrading to 2.0.0 see the :doc:`notes </upgrading/1_to_2>`.

+ [CORE_ENHANCEMENTS] Lots of core enhancements, too many to document
+ [CORE_ENHANCEMENTS] Changes on how the inventory
+ [CORE_ENHANCEMENTS] New ``F`` object for advanced filtering of hosts :doc:`docs </howto/advanced_filtering>`
+ [CORE_ENHANCEMENTS] Improvements on how to serialize/deserialize user facing data like the configuration and the inventory
+ [CORE_ENHANCEMENTS] Connections are now their own type of plugin
+ [CORE_ENHANCEMENTS] Ability to handle connections manually :doc:`docs </howto/handling_connections>`
+ [CORE_BUGFIX] Lots
+ [PLUGIN_BUGFIX] Lots
+ [PLUGIN_NEW] netmiko_save_config
+ [PLUGIN_NEW] echo_data

1.1.0 - July 12 2018
------------------------

+ [PLUGIN_IMPROVEMENT] print_result is now thread safe :issue:`182`
+ [DOCUMENTATION] Minor fixes to documentation :issue:`179` :issue:`178` :issue:`153`:issue:`148` :issue:`145`
+ [TESTS] replace nsot container with requests-mock :issue:`172`
+ [PLUGIN_IMPROVEMENT] Support SSH Agent forwarding for paramiko SSH connections :issue:`159`
+ [PLUGIN_IMPROVEMENT] allow passing options to napalm getters :issue:`156`
+ [PLUGIN_BUGFIX] Fix for SSH and API port mapping issues :issue:`154`
+ [CORE_NEW_FEATURE] add to_dict function so the inventory is serializable :issue:`146`
+ [CORE_BUGFIX] Fix issues with using built-in and overwriting variable with loop variable :issue:`144`


1.0.1 - May 16 2018
------------------------

+ [CORE] Rename brigade to nornir :issue:`139`


1.0.0 - May 4 2018
------------------------

+ [CORE] First release
