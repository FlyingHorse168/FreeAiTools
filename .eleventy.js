module.exports = function(eleventyConfig) {
    // 允许 11ty 处理 MD 文件
    eleventyConfig.addPassthroughCopy("*.md");
    // 忽略 WorkBuddy 项目数据目录，避免其 md 被当作 Liquid 模板解析
    eleventyConfig.ignores.add(".workbuddy/**");
    // 设置默认模板引擎为 MD
    return {
      markdownTemplateEngine: "liquid",
      htmlTemplateEngine: "liquid"
    };
  };