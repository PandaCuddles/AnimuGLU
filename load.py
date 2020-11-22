import sql_cmd
from jikan_controller import Animu


def load_library(conn, lib_type, sort):
    
    results = sql_cmd.load(conn, lib_type.lower(), sort)
        
    if results:
        library = []
        name_list = []
        for item in results:
            animu = Animu(item, item["search_type"], True)
            library.append(animu)
            if sort < 2:
                # Format names for unsorted/sorted by name
                if len(animu.title) > 28:
                    name_list.append(f"{animu.title[:28]}.. [{animu.type}]")
                else:
                    name_list.append(f"{animu.title} [{animu.type}]")
            else:
                # Format names for sorted by type
                if len(animu.title) > 28:
                    name_list.append(f"[{animu.type}] {animu.title[:28]}..")
                else:
                    name_list.append(f"[{animu.type}] {animu.title}")

        return name_list, library

    else:
        return None, None
