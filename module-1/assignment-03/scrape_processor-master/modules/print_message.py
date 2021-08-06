def print_message(message: str,log_file=None, verbose=False, log=False):
        """
        Helper function for printing and\or logging information about scraping
        Assumes:
                message - string
                verbose, log - bool representing verbose/log options
        Returns:
                none
        """
        if verbose: print(message)
        if log: log_file.writelines([message])
    