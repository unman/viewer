# viewer

Basic Qubes network viewer, using networkx, and stripped networkx_viewer  
Use on management qube  
Displays Qubes network configuration - allows user to control qubes (start/shutdown).  
Uses appropriate label colours  
Highlights any Templates that are connected to a netvm  
Change display name, hide or highlight qubes and paths for sharing.  
Roll over to display qube information.

Obligatory screenshot:  
![Screenshot](screenshot.png)


Install networkx, networkx_viewer  
Generate data file from:  
`qvm-ls -O name,netvm,label,klass,template,IP,IPBACK,GATEWAY,visible_ip,visible_netmask,visible_gateway --raw-data >> list11`

To start/shutdown qubes, edit the permission files in /etc/qube-rpc/policy/ -   
admin.vm.Start and admin.vm.Shutdown  
Or use `include/admin-global-rwx`  
To have read only permissions, edit `include/admin-global-ro` 

TBD: Add to action menus - qvm-prefs?  
TBD: Add ability to create notes  
TBD: Remove nulls- - they are weighting the display badly and confuse - why is 'None' treated as a node?  
TBD: Show status.  
TBD: Make graph update  
TBD: Make interactive control - drag node to change netvm?  
TBD: Make interactive control - Select Edge to configure firewall?
