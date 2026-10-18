from django.shortcuts import render
from models.versions import find_version_by_id
from storage import load_data_from_all_files


def version_list(request):
    """Отображает журнал версий электронных документов со статусом ЭЦП."""
    _, _, _, versions = load_data_from_all_files()
    context = {
        "versions": versions,
    }
    return render(request, "versions/version_list.html", context)


def version_detail(request, ver_id: int):
    """Отображает детальную карточку редакции документа."""
    _, _, _, versions = load_data_from_all_files()
    version = find_version_by_id(versions, ver_id)

    context = {
        "version": version,
    }
    return render(
        request,
        "versions/version_detail.html",
        context,
        status=404 if version is None else 200,
    )
