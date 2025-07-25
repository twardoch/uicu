# User Guide

Welcome to the UICU User Guide! This comprehensive guide will help you master Unicode text processing with UICU.

## Guide Overview

The guide is organized to take you from basic concepts to advanced usage:

### 📚 Foundation
- **[Unicode Basics](unicode-basics.md)** - Essential Unicode concepts and terminology
- **[Character Properties](character-properties.md)** - Analyzing and understanding Unicode characters

### 🌍 Internationalization
- **[Locale Management](locale-management.md)** - Working with locales and cultural conventions
- **[Text Collation](text-collation.md)** - Locale-aware sorting and comparison

### ✂️ Text Processing
- **[Text Segmentation](text-segmentation.md)** - Breaking text into meaningful units
- **[Transliteration](transliteration.md)** - Converting between scripts and transforming text

### 📅 Formatting
- **[Date/Time Formatting](date-time-formatting.md)** - Locale-aware date and time display

### 💡 Best Practices
- **[Best Practices](best-practices.md)** - Tips for effective UICU usage

## Quick Navigation

=== "By Feature"

    | Feature | Description | Guide Page |
    |---------|-------------|------------|
    | Character Info | Get Unicode properties | [Character Properties](character-properties.md) |
    | Sorting | Locale-aware collation | [Text Collation](text-collation.md) |
    | Text Breaking | Words, sentences, graphemes | [Text Segmentation](text-segmentation.md) |
    | Script Conversion | Transliteration | [Transliteration](transliteration.md) |
    | Locales | Cultural conventions | [Locale Management](locale-management.md) |
    | Date Formatting | Locale-specific dates | [Date/Time Formatting](date-time-formatting.md) |

=== "By Use Case"

    | Use Case | Relevant Guides |
    |----------|-----------------|
    | Building a multilingual app | [Locales](locale-management.md), [Collation](text-collation.md), [Formatting](date-time-formatting.md) |
    | Processing user input | [Segmentation](text-segmentation.md), [Character Properties](character-properties.md) |
    | Converting between scripts | [Transliteration](transliteration.md) |
    | Analyzing text | [Unicode Basics](unicode-basics.md), [Character Properties](character-properties.md) |
    | Sorting names/data | [Text Collation](text-collation.md) |

## Learning Path

### 🎯 For Beginners
1. Start with [Unicode Basics](unicode-basics.md) to understand fundamental concepts
2. Learn about [Character Properties](character-properties.md)
3. Explore [Text Segmentation](text-segmentation.md) for basic text processing
4. Try simple [Transliteration](transliteration.md) examples

### 🚀 For Intermediate Users
1. Master [Locale Management](locale-management.md) for internationalization
2. Implement proper [Text Collation](text-collation.md) for your data
3. Use advanced [Segmentation](text-segmentation.md) features
4. Format dates with [Date/Time Formatting](date-time-formatting.md)

### 💪 For Advanced Users
1. Optimize performance with [Best Practices](best-practices.md)
2. Handle edge cases in all areas
3. Build custom transformation chains
4. Implement complex locale hierarchies

## Key Concepts

Before diving into specific features, understand these core concepts:

### Unicode vs. Encodings
- **Unicode**: Universal character set assigning unique numbers to characters
- **UTF-8/UTF-16**: Encodings that represent Unicode in bytes
- **Code Points**: Unique numbers assigned to characters (U+0041 for 'A')
- **Grapheme Clusters**: User-perceived characters (may be multiple code points)

### Locale Awareness
- **Locale**: Combination of language, region, and cultural conventions
- **Collation**: Locale-specific sorting rules
- **Formatting**: Locale-specific display conventions
- **Segmentation**: Language-specific text breaking rules

### ICU Foundation
UICU is built on ICU (International Components for Unicode), providing:
- Industry-standard Unicode implementation
- Comprehensive locale data
- Proven algorithms and performance
- Regular updates for new Unicode versions

## Common Tasks

### "How do I...?"

<div class="grid cards" markdown>

-   **Sort names correctly?**
    
    See [Text Collation](text-collation.md#sorting-names)

-   **Handle emojis?**
    
    See [Character Properties](character-properties.md#emoji-handling)

-   **Break Thai text into words?**
    
    See [Text Segmentation](text-segmentation.md#thai-word-breaking)

-   **Convert Cyrillic to Latin?**
    
    See [Transliteration](transliteration.md#script-conversion)

-   **Format dates for different countries?**
    
    See [Date/Time Formatting](date-time-formatting.md#locale-specific-formatting)

-   **Detect text direction?**
    
    See [Character Properties](character-properties.md#bidirectional-text)

</div>

## Tips for Using This Guide

1. **Code Examples**: All examples are complete and runnable
2. **Progressive Complexity**: Each guide starts simple and builds up
3. **Cross-References**: Links connect related topics
4. **Real-World Focus**: Examples use practical scenarios
5. **Performance Notes**: Look for ⚡ symbols for performance tips

## Getting Help

- **API Details**: See the [API Reference](../api/index.md)
- **Working Examples**: Check the [Examples](../examples/index.md) section
- **Common Issues**: Read [Best Practices](best-practices.md)
- **Community**: Visit our [GitHub Discussions](https://github.com/twardoch/uicu/discussions)

Ready to start? Begin with [Unicode Basics](unicode-basics.md) →