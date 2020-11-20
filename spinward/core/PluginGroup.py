class PluginGroup(type):
	"""
	Metaclass for plugin groups.
	Based on Marty Alchin's Simple Plugin Framework (http://martyalchin.com/2008/jan/10/simple-plugin-framework/)
	"""

	_VIRTUAL_BASE = False


	def __init__(cls, name, bases, attrs):
		if not hasattr(cls, 'plugins'):
			# This branch only executes when processing the mount point itself.
			# So, since this is a new plugin type, not an implementation, this
			# class shouldn't be registered as a plugin. Instead, it sets up a
			# list where plugins can be registered later.
			cls.plugins = []
		else:
			# This must be a plugin implementation, which should be registered.
			# Simply appending it to the list is all that's needed to keep
			# track of it later.

			# Only record leaf classes, not intermediate, virtual base classes.
			if not cls._VIRTUAL_BASE:
				cls.plugins.append(cls)
		print("cls.plugins = %r" % (cls.plugins,))	##### DEBUG ######


	def get_plugins(cls, *args, **kwargs):
		"""
        @param args:    Positional args for plugins
        @param kwargs:  Keyword args for plugins

		@return list containing one instance of each plugin in this PluginGroup.
		"""
		return [p(*args, **kwargs) for p in cls.plugins]


	def get_plugin_classes(cls):
		"""
		@return list of plugin classes in this PluginGroup
		"""
		# Return a copy so caller can't modify original.
		return cls.plugins[:]


	def get_plugin_names(cls):
		"""
		@return list of names (strings) of plugins in this PluginGroup
		"""
		return [ p._PLUGIN_NAME for p in cls.plugins ]


	def get_plugin_class_by_name(cls, pluginName):
		"""
		@param pluginName:	Name of plugin for which to return class.

		@return plugin class matching the specified name, or None if no match
		"""
		classes = [ p for p in cls.plugins if p._PLUGIN_NAME == pluginName ]
		if classes:
			return classes[0]
		return None


	def get_plugin_by_name(cls, pluginName, *args, **kwargs):
		"""
		@param pluginName:	Name of plugin for which to return an instance.

		@return instance of plugin class matching the specified name, or None if no match
		"""
		plugin_class= cls.get_plugin_class_by_name(pluginName)
		if plugin_class:
			return plugin_class(*args, **kwargs)
		return None
