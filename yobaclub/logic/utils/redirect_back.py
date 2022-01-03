from django.shortcuts import redirect

def redirect_back_or_index(request) -> None:
    previous_page = request.META.get("HTTP_REFERER")
    if previous_page is not None:
        previous_page =  previous_page.split('/')[-1]
        if len(previous_page) > 2 and not previous_page.isspace() and previous_page != "logout":
            previous_page = previous_page.replace("-", "_")
            return redirect(previous_page)
    return redirect('index')