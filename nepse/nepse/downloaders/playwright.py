from scrapy_playwright.handler import ScrapyPlaywrightDownloadHandler

async def block_unwanted_resources(route, request):
    if request.resource_type in ["image", "font", "stylesheet"]:
        await route.abort()
    else:
        await route.continue_()

class OptimizedPlaywrightDownloadHandler(ScrapyPlaywrightDownloadHandler):
    pass

    async def _create_page(self, request, context, spider):
        page = await super()._create_page(request, context, spider)
        await page.route("**/*", block_unwanted_resources)
        return page
