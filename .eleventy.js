module.exports = function(eleventyConfig) {
    // 允许 11ty 处理 MD 文件
    eleventyConfig.addPassthroughCopy("*.md");
    // 设置默认模板引擎为 MD
    return {
      markdownTemplateEngine: "liquid",
      htmlTemplateEngine: "liquid"
    };
  };