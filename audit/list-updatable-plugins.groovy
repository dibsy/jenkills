def plugin_lists = new ArrayList(Jenkins.instance.pluginManager.plugins)

for (plugin in plugin_lists){
  if(plugin.hasUpdate()){
   	println plugin.getDisplayName()+" need update with version "+ plugin.getUpdateInfo().version
  }
}
