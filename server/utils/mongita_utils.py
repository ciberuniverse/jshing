def project(result_mongita: dict|list, project: dict) -> dict:

    def filter_mini(document: dict, project_: dict):
        for name_key, to_hiddisplay in project_.items():
            
            if not to_hiddisplay:
                document.pop(name_key)

        return document

    # Si el resultado es un iterable de mongita db        
    if isinstance(result_mongita, list):

        # Nuevo resultado
        new_result = []
        # Se recorre modificando cada elemento del array al deseado
        for element in result_mongita:
            
            new_result.append(filter_mini(element, project))

        return new_result
    
    return filter_mini(result_mongita, project)