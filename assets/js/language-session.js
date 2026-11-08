(function () {
  var feedback = document.getElementById("translation-feedback");
  var profileImages = document.querySelectorAll("[data-profile-image]");
  var languageSwitchers = document.querySelectorAll("[data-language-switcher]");

  // Show translation-unavailable banner when redirected with ?translation=unavailable param.
  function showFeedbackIfNeeded() {
    if (!feedback) return;

    var url = new URL(window.location.href);
    var translationParam = url.searchParams.get("translation");
    if (translationParam !== "unavailable") return;

    var activeLocale = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
    var message = activeLocale === "es"
      ? (feedback.dataset.messageEs || feedback.dataset.messageEn)
      : feedback.dataset.messageEn;

    feedback.textContent = message;
    feedback.hidden = false;

    // Clean the query params from the URL without reloading.
    var cleanUrl = new URL(window.location.href);
    cleanUrl.searchParams.delete("translation");
    cleanUrl.searchParams.delete("requested");
    cleanUrl.searchParams.delete("fallback_attempt");
    window.history.replaceState({}, "", cleanUrl.toString());
  }

  function stripFallbackQueryParams(url) {
    url.searchParams.delete("translation");
    url.searchParams.delete("requested");
    url.searchParams.delete("fallback_attempt");
    return url;
  }

  function revealImageFallback(imageElement) {
    if (!imageElement) return;

    var fallbackTargetId = imageElement.getAttribute("data-fallback-target");
    if (!fallbackTargetId) return;

    var fallbackNode = document.getElementById(fallbackTargetId);
    imageElement.classList.add("is-hidden");

    if (fallbackNode) {
      fallbackNode.hidden = false;
    }
  }

  function setupProfileImageFallbacks() {
    if (!profileImages.length) return;

    profileImages.forEach(function (imageElement) {
      imageElement.addEventListener("error", function () {
        revealImageFallback(imageElement);
      });

      if (imageElement.complete && imageElement.naturalWidth === 0) {
        revealImageFallback(imageElement);
      }
    });
  }

  // Build locale switch targets from the current URL first, then fallback to data-target values.
  function buildLocalePathFromCurrentUrl(targetLang, languageSwitcher) {
    var url = new URL(window.location.href);
    var path = url.pathname;
    var baseUrl = languageSwitcher
      ? languageSwitcher.getAttribute("data-baseurl") || ""
      : "";

    // Normalize to avoid accidental double slashes while preserving root.
    path = path.replace(/\/+/g, "/");
    baseUrl = baseUrl.replace(/\/+/g, "/").replace(/\/$/, "");
    if (baseUrl && (path === baseUrl || path.indexOf(baseUrl + "/") === 0)) {
      path = path.slice(baseUrl.length) || "/";
    }
    if (path !== "/" && path.endsWith("/")) {
      path = path.slice(0, -1);
    }

    var isSpanishPath = path === "/es" || path.indexOf("/es/") === 0;
    var basePath = isSpanishPath ? path.replace(/^\/es/, "") : path;
    if (!basePath) {
      basePath = "/";
    }

    var targetPath = targetLang === "es"
      ? (basePath === "/" ? "/es/" : "/es" + basePath)
      : basePath;

    var params = new URLSearchParams(url.search);
    params.delete("translation");
    params.delete("requested");
    params.delete("fallback_attempt");

    var query = params.toString();
    return baseUrl + targetPath + (query ? "?" + query : "") + url.hash;
  }

  function resolveSwitcherTarget(languageSwitcher, targetLang) {
    if (!languageSwitcher) return buildLocalePathFromCurrentUrl(targetLang, languageSwitcher);

    var dataAttribute = targetLang === "es" ? "data-target-es" : "data-target-en";
    var serverTarget = languageSwitcher.getAttribute(dataAttribute);
    var translationMode = languageSwitcher.getAttribute("data-translation-mode");

    if (serverTarget) {
      var parsedServerTarget = new URL(serverTarget, window.location.origin);
      var hasExplicitFallback = parsedServerTarget.searchParams.get("translation") === "unavailable";

      if (hasExplicitFallback) {
        // Trust the fallback: template confirmed no equivalent exists for this page.
        return parsedServerTarget.pathname + parsedServerTarget.search + parsedServerTarget.hash;
      }

      if (translationMode === "explicit") {
        // Template used page.translated_url — the target slug differs from the URL in the
        // other locale (e.g. bilingual posts), so trust the server-provided target directly.
        return parsedServerTarget.pathname + parsedServerTarget.search + parsedServerTarget.hash;
      }

      // For computed mode, prefer the server-rendered URL when available to avoid
      // environment-specific path differences between local and production hosts.
      return parsedServerTarget.pathname + parsedServerTarget.search + parsedServerTarget.hash;
    }

    // Default: compute target from current browser URL (works for pages with matching slugs).
    return buildLocalePathFromCurrentUrl(targetLang, languageSwitcher);
  }

  // Fix language switcher href buttons to use current URL-aware targets.
  // This keeps navigation stable across apex/www hostnames while cert propagation finishes.
  function fixLanguageSwitcherHrefs() {
    if (!languageSwitchers.length) return;

    languageSwitchers.forEach(function (languageSwitcher) {
      var targetEn = resolveSwitcherTarget(languageSwitcher, "en");
      var targetEs = resolveSwitcherTarget(languageSwitcher, "es");

      var links = languageSwitcher.querySelectorAll("a[data-language-option]");
      links.forEach(function (link) {
        var lang = link.getAttribute("data-language-option");
        if (lang === "en") {
          link.href = targetEn;
        } else if (lang === "es") {
          link.href = targetEs;
        }
      });
    });
  }

  showFeedbackIfNeeded();
  setupProfileImageFallbacks();
  fixLanguageSwitcherHrefs();
})();
