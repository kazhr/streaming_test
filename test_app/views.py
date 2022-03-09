import time
from django.http import StreamingHttpResponse
from django.template import loader


def long_task(request):
    """
    何らかの繰り返し処理の結果を毎ループごとに出力
    """
    for i in range(10):
        # 何らかの重たい処理の代わりにsleep
        time.sleep(1)
        yield i


def index(request):
    """
    結果を素のまま表示
    """
    return StreamingHttpResponse(
        long_task(request),
    )


def generate_html(request):
    """
    long_taskの結果を箇条書きで出力
    """
    yield "<!DOCTYPE html>\n"
    yield "<html>\n"
    yield "<head></head>\n"
    yield "<body>\n"
    yield "  <h1>results</h1>\n"
    yield "  <ul>\n"
    for s in long_task(request):
        yield f"    <li>{s}</li>\n"
    yield "  </ul>\n"
    yield "  <hr>\n"
    yield "  end\n"
    yield "</body>\n"
    yield "</html>"


def with_html(request):
    """
    結果をhtmlで表示
    """
    return StreamingHttpResponse(
        generate_html(request),
    )


def generate_html_with_java(request):
    """
    先にendまで出力してから、jQueryを使用して
    long_taskの結果を箇条書きに追加
    """
    yield "<!DOCTYPE html>\n"
    yield "<html>\n"
    yield "<head>\n"
    yield "  <script src='https://code.jquery.com/jquery-3.6.0.min.js' integrity='sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=' crossorigin='anonymous'></script>\n"
    yield "</head>\n"
    yield "  <body>\n"
    yield "  <h1>results</h1>\n"
    yield "  <ul id='results'>\n"
    yield "  </ul>\n"
    yield "  <hr>\n"
    yield "  end\n"
    for s in long_task(request):
        yield f"  <script>$('#results').append('<li>{s}</li>');</script>\n"
    yield "</body>\n"
    yield "</html>"


def with_java(request):
    """
    結果をhtmlとjavascriptで表示
    """
    return StreamingHttpResponse(
        generate_html_with_java(request),
    )


def generate_html_from_template(request):
    """
    templateからhtmlを作成
    """
    template = loader.get_template("test_app/template.html")
    context = {"title": "templateを使用"}
    html = template.render(context, request)

    # -3行目まで表示
    for line in html.split("\n")[:-3]:
        yield f"{line}\n"

    # 結果を差し込む
    for s in long_task(request):
        yield f"  <script>$('#results').append('<li>{s}</li>');</script>\n"

    # 残りを表示
    for line in html.split("\n")[-2:]:
        yield f"{line}\n"


def with_template(request):
    """
    結果をtemplateを使用して表示
    """
    return StreamingHttpResponse(
        generate_html_from_template(request),
    )
