# binja-msdn
Author: **Benedikt Schmotzle**

Binary Ninja plugin to query MSDN api documentation.

## Description:

This plugin tries to ease up the process of querying the documentation of a 
Win32 API function while reversing in Binary Ninja. When run it asks the user
for a query string and opens the first resulting link inside a new html report
view within Binary Ninja.

## Required Dependencies

The following dependencies are required for this plugin:

 * pip requests
 * pip beautifulsoup4

## Install

Simply run
```
$ git clone https://github.com/schmotzle/binja-msdn ~/.binaryninja/plugins/binja-msdn
```

## Screenshots

![Query field](https://github.com/schmotzle/blog/blob/gh-pages/share/recv_query.png?raw=true)

![Query result](https://github.com/schmotzle/blog/blob/gh-pages/share/recv_result.png?raw=true)


## License

This plugin is released under a [MIT](LICENSE) license.
