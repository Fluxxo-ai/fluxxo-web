import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    seoTitle: z.string().optional(),
    seoDescription: z.string().optional(),
    category: z.string(),
    icon: z.string().optional(),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    readTime: z.string(),
    pubDate: z.date(),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
