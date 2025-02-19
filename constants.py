SONG_SEARCH_BAR_PLACEHOLDER = "Search song..."

HELP_AND_INFORMATION_TEXT = (
        "--------Help & Information--------\n\n" +

        "--------------------------------------------------------------------------------------------------------\n\n"
        
        "----Overview----\n" +

        "Echo Library is a music metadata management application designed to help users organise, view, " +
        "and track music they have browsed while exploring for new songs.\n\n"

        "It's specially designed to help you track songs you’ve already come across in your search for new music. " +
        "By maintaining a database of every song that’s dragged into the app, it provides a clear view of what " +
        "you’ve already browsed and helps you focus on undiscovered music. For instance, if you drag in a song " +
        "you’ve already encountered, Echo Library flags it as a duplicate, letting you know that it’s already in " +
        "your collection. This way, you can avoid listening to the same song twice while browsing for new music.\n\n" +

        "One of the key data points highlighted within Echo Library is the approximate release date. The app " +
        "extracts this information for each song, making it easy to identify the latest tracks.\n\n"
        
        "--------------------------------------------------------------------------------------------------------\n\n"

        "----Functionality----\n"
        
        "The app enables users to drag and drop folders containing `.m4p` files directly into the interface. " +
        "The app's design aligns with Apple Music's file storage structure on Mac, where songs are organised in a " +
        "nested folder format by artist and then album, with the song file (song.m4p) stored within " +
        "(artist/album/song.m4p). Note that individual `.m4p` files cannot be dragged into the interface; only " +
        "folders are supported.\n\n"

        "Once a folder is dragged into the interface, the app automatically extracts key metadata from each song " +
        "and displays it in a clean, tabular format. The main screen includes several useful features, such as the " +
        "option to remove selected songs from the imported list and the ability to export all the data within the " +
        "main view to excel.\n\n"

        "Behind the scenes, each song’s metadata is saved to a database when you import a song folder. " +
        "While the metadata on the main screen is available only for the current session, the data in the database " +
        "is stored persistently until you choose to remove it. To access your full `browsed` music library, you can " +
        "use the `Open Database Viewer` button, which provides a complete view of all previously imported songs. " +
        "The database viewer also offers features to search for specific songs, delete selected songs entirely from " +
        "the database, and export all data to Excel for further analysis.\n\n"
        
        "--------------------------------------------------------------------------------------------------------\n\n"

        "----Handling Errors within the Drag and Drop Window----\n"
        
        "If an error occurs while using the drag-and-drop feature in Echo Library, it’s helpful to understand" +
        " how the app handles folder imports. Unlike a typical import sequence, Echo Library imports folders in " +
        "reverse order, starting from the top of your selected files rather than the bottom.\n\n"
        
        "This isn’t an issue unless an error disrupts the import. When that happens, it’s easy to lose track of " +
        "your progress.\n\n"
        
        "For example, say you have five existing folders already imported and are now adding five more. " +
        "In Finder/File Explorer, they might look like the following section (Finder/File Explorer Order).\n\n"
        
        "--Finder/File Explorer Order--\n"
        "-Little Mix\n"
        "-Skepta\n"
        "-Giggs"
        "-5SOS\n"
        "-Luke Combs\n"
        "-Stormzy\n"
        "-Zayn\n"
        "-Niall Horan\n"
        "-Justin Bieber\n"
        "-Harry Styles\n\n"
        
        "--Existing Folders (how they appear in Echo Library)--\n"
        "-Harry Styles\n"
        "-Justin Bieber\n"
        "-Niall Horan\n"
        "-Zayn\n"
        "-Stormzy\n\n"
        
        "--New Import Folders (imported order)--\n"
        "-Little Mix\n"
        "-Skepta\n"
        "-Giggs                 <—ERROR\n"
        "-5SOS\n"
        "-Luke Combs\n\n"
        
        "If the import encounters an error on the 'Giggs' folder, the app will import only 'Little Mix' and " +
        "'Skepta', terminating at 'Giggs' due to the error. It won't even get to either '5SOS' or 'Luke Combs.'\n\n"
        
        "--New Folders (how the two imported folders will appear in the app)--\n"
        "-Little Mix             <-- NEW\n"
        "-Skepta                <-- NEW\n"
        "-Harry Styles\n"
        "-Justin Bieber\n"
        "-Niall Horan\n"
        "-Zayn\n"
        "-Stormzy\n\n"
        
        "To avoid issues, remember the last imported folder before beginning your next batch. In this case, note " +
        "that 'Harry Styles' was your last existing folder, and 'Luke Combs' is the final folder in your import " +
        "batch.\n\n"
        
        "By following these steps, you’ll be able to track your imports accurately and resume smoothly if an error " +
        "occurs.\n\n"

        "--------------------------------------------------------------------------------------------------------\n\n"

        "----Error Log----\n"

        "The Error Log tracks errors encountered during folder processing within the application. Occasionally, " +
        "some music folders may not upload successfully. However, the Error Log allows you to monitor all " +
        "unsuccessful uploads to the application, with the added ability to export all error logs for easier " +
        "tracking and troubleshooting.\n\n"
        
        "--------------------------------------------------------------------------------------------------------\n\n"
)
