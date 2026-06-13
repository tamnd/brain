export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Redirect legacy /en/* paths (old Hugo multilingual URLs) to root-relative equivalents
    if (url.pathname === "/en" || url.pathname.startsWith("/en/")) {
      const newPath = url.pathname.startsWith("/en/") ? url.pathname.slice(3) : "/";
      const redirectUrl = new URL(url);
      redirectUrl.pathname = newPath || "/";
      return Response.redirect(redirectUrl.toString(), 301);
    }

    const accept = request.headers.get("Accept") ?? "";
    const wantsMarkdown = accept.split(",").some(part => {
      const [type] = part.trim().split(";");
      return type.trim() === "text/markdown";
    });

    if (wantsMarkdown) {
      const repoName = url.hostname.split(".")[0];
      const contentBase = repoName === "brain" ? "content/en" : "content";
      const rawBase = `https://raw.githubusercontent.com/tamnd/${repoName}/main/${contentBase}`;

      const pathname = url.pathname.endsWith("/") ? url.pathname : url.pathname + "/";
      const indexUrl = rawBase + pathname + "_index.md";

      const check = await fetch(indexUrl, { method: "HEAD" });
      if (check.ok) {
        return Response.redirect(indexUrl, 302);
      }

      const leafUrl = rawBase + pathname.slice(0, -1) + ".md";
      return Response.redirect(leafUrl, 302);
    }

    const res = await env.ASSETS.fetch(request);
    if ((res.headers.get("Content-Type") ?? "").includes("text/html")) {
      const headers = new Headers(res.headers);
      headers.set("Vary", "Accept");
      return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
    }
    return res;
  },
};
