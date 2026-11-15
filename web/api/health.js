// GET /api/health：不用口令的体检。只回答：GitHub token 能不能读、能不能写，口令有没有设。不返回任何内容。
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
      // 写权限：故意带一个不存在的版本号去写 README.md。有写权限时 GitHub 因版本号对不上拒绝（409/422），不会产生提交；没有写权限是 403。
      const w = await fetch(`https://api.github.com/repos/${STATIC.repo.owner}/${STATIC.repo.name}/contents/README.md`, {
        method: "PUT",
        headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}`, Accept: "application/vnd.github+json", "User-Agent": "rebuttal-workbench" },
        body: JSON.stringify({ message: "probe", content: Buffer.from("probe").toString("base64"), sha: "0".repeat(40), branch: STATIC.repo.branch }),
      });
      out.write = w.status === 409 || w.status === 422;
      if (!out.write) out.writeStatus = w.status;
    } catch (e) { out.tokenStatus = "network"; }
  }
  res.status(200).json(out);
};
