// GET /api/health：不用口令的体检。只回答两件事：GitHub token 能不能读到仓库、口令有没有设。不返回任何内容。
const { STATIC } = require("./_lib.js");

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  const out = { token: false, passcode: !!process.env.PASSCODE };
  if (process.env.GITHUB_TOKEN) {
    try {
      const r = await fetch(`https://api.github.com/repos/${STATIC.repo.owner}/${STATIC.repo.name}/commits?per_page=1`, {
        headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}`, Accept: "application/vnd.github+json", "User-Agent": "rebuttal-workbench" },
      });
      out.token = r.status === 200;
      if (!out.token) out.tokenStatus = r.status;
    } catch (e) { out.tokenStatus = "network"; }
  }
  res.status(200).json(out);
};
