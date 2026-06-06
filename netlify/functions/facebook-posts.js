const PAGE_ID = process.env.FACEBOOK_PAGE_ID || "";
const ACCESS_TOKEN = process.env.FACEBOOK_PAGE_ACCESS_TOKEN || "";
const GRAPH_VERSION = process.env.FACEBOOK_GRAPH_VERSION || "v20.0";

function normalizePost(post) {
  return {
    id: post && post.id ? String(post.id) : "",
    message: post && (post.message || post.story) ? String(post.message || post.story) : "",
    image: post && post.full_picture ? String(post.full_picture) : "",
    url:
      post && post.permalink_url
        ? String(post.permalink_url)
        : `https://www.facebook.com/${PAGE_ID}`,
    createdTime: post && post.created_time ? String(post.created_time) : ""
  };
}

exports.handler = async function handler() {
  if (!PAGE_ID || !ACCESS_TOKEN) {
    return {
      statusCode: 503,
      headers: {
        "content-type": "application/json; charset=utf-8",
        "cache-control": "no-store"
      },
      body: JSON.stringify({
        posts: [],
        source: "missing-credentials"
      })
    };
  }

  try {
    const apiUrl = new URL(`https://graph.facebook.com/${GRAPH_VERSION}/${PAGE_ID}/posts`);
    apiUrl.searchParams.set("fields", "message,full_picture,permalink_url,created_time,story");
    apiUrl.searchParams.set("limit", "6");
    apiUrl.searchParams.set("access_token", ACCESS_TOKEN);

    const response = await fetch(apiUrl.toString(), {
      headers: {
        accept: "application/json"
      }
    });

    const payload = await response.json();
    const posts = Array.isArray(payload && payload.data)
      ? payload.data.slice(0, 6).map(normalizePost)
      : [];

    if (!response.ok) {
      return {
        statusCode: response.status,
        headers: {
          "content-type": "application/json; charset=utf-8",
          "cache-control": "public, max-age=120, stale-while-revalidate=600"
        },
        body: JSON.stringify({
          posts: [],
          source: "facebook-error",
          error: payload && payload.error ? payload.error.message || "Facebook API error" : "Facebook API error"
        })
      };
    }

    return {
      statusCode: 200,
      headers: {
        "content-type": "application/json; charset=utf-8",
        "cache-control": "public, max-age=300, stale-while-revalidate=3600"
      },
      body: JSON.stringify({
        posts,
        source: "facebook"
      })
    };
  } catch (error) {
    return {
      statusCode: 502,
      headers: {
        "content-type": "application/json; charset=utf-8",
        "cache-control": "no-store"
      },
      body: JSON.stringify({
        posts: [],
        source: "fetch-failed",
        error: error && error.message ? error.message : "Unable to load Facebook posts"
      })
    };
  }
};
