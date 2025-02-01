# Echo Library

## Overview
Echo Library is a music metadata management application designed to help users organise, view, and track music they 
have browsed while exploring for new songs.

It's specially designed to help you track songs you’ve already come across in your search for new music. 
By maintaining a database of every song that’s dragged into the app, it provides a clear view of what 
you’ve already browsed and helps you focus on undiscovered music. For instance, if you drag in a song 
you’ve already encountered, Echo Library flags it as a duplicate, letting you know that it’s already in 
your collection. This way, you can avoid listening to the same song twice while browsing for new music.

One of the key data points highlighted within Echo Library is the approximate release date. The app extracts this 
information for each song, making it easy to identify the latest tracks.

## Functionality
The app enables users to drag and drop folders containing `.m4p` files directly into the interface.
The app's design aligns with Apple Music's file storage structure on Mac, where songs are organised in a
nested folder format by artist and then album, with the song file (song.m4p) stored within
(artist/album/song.m4p). Note that individual `.m4p` files cannot be dragged into the interface; only
folders are supported."

Once a folder is dragged into the interface, the app automatically extracts key metadata from each song
and displays it in a clean, tabular format. The main screen includes several useful features, such as the
option to remove selected songs from the imported list and the ability to export all the data within the
main view to excel.

Behind the scenes, each song’s metadata is saved to a database when you import a song folder.
While the metadata on the main screen is available only for the current session, the data in the database
is stored persistently until you choose to remove it. To access your full browsed music library, you can
use the `Open Database Viewer` button, which provides a complete view of all previously imported songs.
The database viewer also offers features to search for specific songs, delete selected songs entirely from 
the database, and export all data to Excel for further analysis.

## Handling Errors within the Drag and Drop Window

If an error occurs while using the drag-and-drop feature in Echo Library, it’s helpful to understand how the app 
handles folder imports. Unlike a typical import sequence, Echo Library imports folders in reverse order, starting from the top
of your selected files rather than the bottom.

This isn’t an issue unless an error disrupts the import. When that happens, it’s easy to lose track of your progress.

For example, say you have five existing folders already imported and are now adding five more. 
In Finder/File Explorer, they might look like the following section (Finder/File Explorer Order).

### Already Imported Folders - Echo Library Order
        -Stormzy
        -Zayn
        -Niall Horan
        -Justin Bieber 
        -Harry Styles
        
### New Folders Required for Importing (top 5) - Finder/File Explorer Order
        -Little Mix
        -Skepta
        -Giggs
        -5SOS
        -Luke Combs
        -Stormzy
        -Zayn
        -Niall Horan
        -Justin Bieber 
        -Harry Styles

### New Imported Folders - Error Occurred
        -Little Mix
        -Skepta
        -Giggs      <—- ERROR
        -5SOS
        -Luke Combs

If the import encounters an error on the “Giggs” folder, the app will import only “Little Mix” and “Skepta”, 
terminating at “Giggs” due to the error.

### New Imported Folders - Echo Library Order
        -Little Mix     <-- NEW
        -Skepta         <-- NEW
        -Stormzy
        -Zayn
        -Niall Horan
        -Justin Bieber 
        -Harry Styles

### Folders Not Imported (due to error) - Finder/File Explorer Order
        -Little Mix
        -Skepta
        -Giggs        <-- NOT IMPORTED
        -5SOS         <-- NOT IMPORTED
        -Luke Combs   <-- NOT IMPORTED        
        -Stormzy
        -Zayn
        -Niall Horan
        -Justin Bieber 
        -Harry Styles

To prevent issues, always note the top and bottom folders in your imported batch before starting the next one. In this case, "Little Mix" was the top folder, and "Luke Combs" was the bottom folder. Since only "Little Mix" and "Skepta" have been imported, this indicates that the folders from "Giggs" (the folder below "Skepta") down to "Luke Combs" were not imported. If an error occurs, it's best to skip the problematic folder and focus on re-importing those that were not processed due to their position. In this example, you would skip "Giggs" (due to its error) and attempt to re-import "5SOS" and "Luke Combs". Any folders that encountered errors can be reviewed at the end of the session in the Error Log (see `Error Log` section below).

By following this approach, you can track your imports more effectively and resume them smoothly if any issues arise.

## Error Log
The Error Log tracks errors encountered during folder processing within the application. Occasionally,
some music folders may not upload successfully. However, the Error Log allows you to monitor all
unsuccessful uploads to the application, with the added ability to export all error logs for easier
tracking and troubleshooting.
