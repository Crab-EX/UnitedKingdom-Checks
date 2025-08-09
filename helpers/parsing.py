def parse_name(full_name: str):
    # Split into Surname and rest
    last_name, rest = [part.strip() for part in full_name.split(",", 1)]
    
    # Split remaining into parts
    name_parts = rest.split()
    first_name = name_parts[0]
    middle_names = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
    
    return first_name, middle_names, last_name