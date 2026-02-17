#
# main.py - Основной файл программы.
#


# Импортируем:
import os
import sys
import json
import shutil


# Основная функция:
def main() -> None:
    argv = sys.argv[1:]
    rh = "build\\tools\\reshack.exe"
    wr = "build\\tools\\windres.exe"
    outdir  = "build/out/"
    if os.path.isdir(outdir): shutil.rmtree(outdir)
    os.mkdir(outdir)

    # Читаем конфиг-файл:
    with open("build/config.json", "r+", encoding="utf-8") as f:
        config = json.load(f)

    # Параметры:
    icon_path          = config["icon-path"]
    company_name       = config["company-name"]
    description        = config["description"]
    file_type          = config["file-type"]  # 1 - .exe | 2 - .dll | 3 - .sys, ... | 4 - Font file.
    file_version       = config["file-version"]
    product_name       = config["product-name"]
    product_version    = config["product-version"]
    legal_copyright    = config["legal-copyright"]
    legal_trademarks   = config["legal-trademarks"]
    file_original_name = config["file-original-name"]
    file_internal_name = config["file-internal-name"]
    path_to_file       = config["path-to-file"]

    # Флаги:
    is_create = False
    is_delete_icon = False
    is_delete_info = False
    is_apply = False

    # Проверяем аргументы:
    for index, arg in enumerate(argv):
        if   arg in ["-create"]:     is_create = True
        elif arg in ["-deleteicon"]: is_delete_icon = True
        elif arg in ["-deleteinfo"]: is_delete_info = True
        elif arg in ["-apply"]:      is_apply = True

    # Создаём:
    if is_create:
        file_ver1 = ",".join([str(v) for v in file_version])
        file_ver2 = ".".join([str(v) for v in file_version])
        product_ver1 = ",".join([str(v) for v in product_version])
        product_ver2 = ".".join([str(v) for v in product_version])
        file = [f"1 ICON \"{icon_path}\"\n" if icon_path else "",
                f"1 ICONGROUP\n",
                f"{{\n",
                f"    1, \"{icon_path}\"\n" if icon_path else "",
                f"}}\n",
                f"1 VERSIONINFO\n",
                f"FILEVERSION     {file_ver1}\n" if file_version else "",
                f"PRODUCTVERSION  {product_ver1}\n" if product_version else "",
                f"FILEOS          0x4\n",
                f"FILETYPE        0x{file_type}\n" if file_type else "",
                f"{{\n",
                f"    BLOCK \"StringFileInfo\"\n",
                f"    {{\n",
                f"        BLOCK \"040904B0\"\n",
                f"        {{\n",
                f"            VALUE \"CompanyName\",      \"{company_name}\"\n"       if company_name       else "",
                f"            VALUE \"FileDescription\",  \"{description}\"\n"        if description        else "",
                f"            VALUE \"FileVersion\",      \"{file_ver2}\"\n"          if file_version       else "",
                f"            VALUE \"InternalName\",     \"{file_internal_name}\"\n" if file_internal_name else "",
                f"            VALUE \"OriginalFilename\", \"{file_original_name}\"\n" if file_original_name else "",
                f"            VALUE \"ProductName\",      \"{product_name}\"\n"       if product_name       else "",
                f"            VALUE \"ProductVersion\",   \"{product_ver2}\"\n"       if product_version    else "",
                f"            VALUE \"LegalCopyright\",   \"{legal_copyright}\"\n"    if legal_copyright    else "",
                f"            VALUE \"LegalTrademarks\",  \"{legal_trademarks}\"\n"   if legal_trademarks   else "",
                f"        }}\n",
                f"    }}\n",
                f"    BLOCK \"VarFileInfo\"\n",
                f"    {{\n",
                f"        VALUE \"Translation\", 0x0409, 1200\n",
                f"    }}\n",
                f"}}\n"
            ]

        # Сохраняем файл:
        with open(os.path.join(outdir, "app.rc"), "w+", encoding="utf-8") as f: f.write("".join(file))

        # Компилируем:
        os.system(f"\"{wr} {os.path.join(outdir, 'app.rc')} -O res -o {os.path.join(outdir, 'app.res')}\"")

    # Удаляем иконку:
    if is_delete_icon:
        os.system(f"\"{rh} -open {path_to_file} -save {path_to_file} -action delete -mask ICONGROUP,,\"")
        os.system(f"\"{rh} -open {path_to_file} -save {path_to_file} -action delete -mask ICON,,\"")

    # Удаляем информацию:
    if is_delete_info:
        os.system(f"\"{rh} -open {path_to_file} -save {path_to_file} -action delete -mask VERSIONINFO,,\"")

    # Применяем конфигурацию:
    if is_apply:
        res = os.path.join(outdir, "app.res")
        os.system(f"\"{rh} -open {path_to_file} -save {path_to_file} -action addoverwrite -res {res}\"")

    # Чистим после работы:
    if os.path.isfile("build/tools/reshack.ini"):
        os.remove("build/tools/reshack.ini")
    if os.path.isdir(outdir): shutil.rmtree(outdir)


# Если этот файл запускают:
if __name__ == "__main__":
    main()
