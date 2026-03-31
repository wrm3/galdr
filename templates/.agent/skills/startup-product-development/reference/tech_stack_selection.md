# Technology Stack Selection Guide

> **Choose the right technologies for your product and team**

## Decision Framework

### Key Selection Criteria

1. **Team Expertise**: What does your team already know?
2. **Time to Market**: How quickly can you ship?
3. **Scalability Needs**: Current vs future scale requirements
4. **Budget**: Upfront and ongoing costs
5. **Ecosystem Maturity**: Community, libraries, tooling
6. **Hiring**: Can you find developers?
7. **Longevity**: Will this tech be around in 5 years?

### Decision Matrix Template

| Technology | Team Know | Speed | Scale | Cost | Ecosystem | Score |
|------------|-----------|-------|-------|------|-----------|-------|
| Option A   | 9/10      | 8/10  | 7/10  | 9/10 | 9/10      | 42/50 |
| Option B   | 5/10      | 9/10  | 9/10  | 6/10 | 8/10      | 37/50 |

**Weighting**: Adjust based on priorities
- Early startup: Emphasize Speed (2x weight)
- Scaling startup: Emphasize Scale (2x weight)

## Software/SaaS Stack

### Frontend

**React** (Recommended for Most)
- **Pros**: Huge ecosystem, easy hiring, component reusability
- **Cons**: Not opinionated, need to choose routing/state management
- **Best for**: Teams with React experience, component-heavy UIs
- **Learning curve**: Medium
- **Example**: Facebook, Airbnb, Netflix

**Next.js** (React Framework - Highly Recommended)
- **Pros**: SSR, file-based routing, API routes, great DX
- **Cons**: Vercel vendor lock-in risk, learning curve
- **Best for**: SEO-critical apps, full-stack React apps
- **Learning curve**: Medium
- **Example**: TikTok, Twitch, Hulu

**Vue.js**
- **Pros**: Easy learning curve, great documentation, lightweight
- **Cons**: Smaller ecosystem than React, less corporate backing
- **Best for**: Small teams, quick MVPs
- **Learning curve**: Low
- **Example**: Alibaba, GitLab, Nintendo

**Svelte/SvelteKit**
- **Pros**: Minimal bundle size, simple syntax, fast performance
- **Cons**: Smaller ecosystem, less job market
- **Best for**: Performance-critical apps, experienced devs
- **Learning curve**: Low-Medium
- **Example**: Spotify (internal tools), NYTimes (graphics)

**Mobile: React Native**
- **Pros**: Code sharing with web (if React), large community
- **Cons**: Native modules can be painful, occasional bugs
- **Best for**: Startups wanting iOS+Android with one codebase

**Mobile: Flutter**
- **Pros**: Beautiful UI, fast performance, single codebase
- **Cons**: Dart language (less popular), larger app size
- **Best for**: UI-heavy apps, teams that know Dart

### Backend

**Node.js** (Express/Fastify)
- **Pros**: JavaScript full-stack, huge package ecosystem (npm)
- **Cons**: Callback hell, weaker typing (use TypeScript)
- **Best for**: Real-time apps, teams with JavaScript expertise
- **Example**: LinkedIn, Netflix, Uber

**Python** (Django/Flask/FastAPI)
- **Pros**: Clean syntax, great for ML/AI, rapid development
- **Cons**: Slower than compiled languages, GIL limits concurrency
- **Best for**: Data/ML products, rapid prototyping
- **Example**: Instagram (Django), Spotify (Flask)

**Go**
- **Pros**: Fast performance, built-in concurrency, simple deployment
- **Cons**: Verbose error handling, smaller ecosystem
- **Best for**: High-performance APIs, microservices
- **Example**: Uber, Twitch, Docker

**Ruby on Rails**
- **Pros**: Convention over configuration, rapid development, mature
- **Cons**: Slower performance, declining popularity
- **Best for**: CRUD-heavy apps, small teams, MVPs
- **Example**: GitHub, Shopify, Airbnb

**Java/Kotlin** (Spring Boot)
- **Pros**: Enterprise-grade, strong typing, JVM performance
- **Cons**: Verbose, slower development, steeper learning curve
- **Best for**: Enterprise B2B, teams with Java background
- **Example**: LinkedIn, Netflix (mixed stack)

### Database

**PostgreSQL** (Recommended for Most)
- **Type**: Relational (SQL)
- **Pros**: ACID, JSON support, mature, open-source, extensions
- **Cons**: Steeper learning curve than MySQL
- **Best for**: Most web apps, complex queries, data integrity critical
- **Managed**: AWS RDS, Google Cloud SQL, Supabase, Railway

**MySQL**
- **Type**: Relational (SQL)
- **Pros**: Simple, widely adopted, great docs
- **Cons**: Less feature-rich than PostgreSQL
- **Best for**: Simple CRUD apps, WordPress-style applications
- **Managed**: AWS RDS, PlanetScale

**MongoDB**
- **Type**: NoSQL (Document)
- **Pros**: Flexible schema, easy to start, JSON-native
- **Cons**: No transactions (pre-4.0), data duplication
- **Best for**: Rapid prototyping, flexible data models
- **Managed**: MongoDB Atlas

**DynamoDB** (AWS)
- **Type**: NoSQL (Key-Value)
- **Pros**: Fully managed, scales automatically, pay per use
- **Cons**: Vendor lock-in, query limitations
- **Best for**: AWS-first teams, serverless architectures

**Firebase Realtime Database / Firestore**
- **Type**: NoSQL (Real-time)
- **Pros**: Real-time sync, auth included, easy setup
- **Cons**: Vendor lock-in, costs scale with usage
- **Best for**: MVPs, real-time apps, mobile backends

### Hosting & Infrastructure

**Vercel** (Frontend Hosting)
- **Best for**: Next.js apps, static sites, quick deployments
- **Pricing**: Free tier generous, $20/mo Pro
- **Pros**: Zero config, edge network, great DX

**Railway** (Full-Stack Hosting)
- **Best for**: Startups, full-stack apps, databases
- **Pricing**: $5/mo minimum, pay for usage
- **Pros**: Simple, databases included, GitHub integration

**AWS** (Amazon Web Services)
- **Best for**: Scaling startups, enterprise
- **Services**: EC2, RDS, S3, Lambda, etc.
- **Pros**: Comprehensive, battle-tested, scalable
- **Cons**: Complex, expensive, steep learning curve

**Google Cloud Platform (GCP)**
- **Best for**: ML/AI products, Google ecosystem
- **Services**: Compute Engine, Cloud SQL, Cloud Storage
- **Pros**: Great ML tools, competitive pricing

**Azure**
- **Best for**: Microsoft stack, enterprise customers
- **Services**: Azure VMs, SQL Database, Blob Storage
- **Pros**: Enterprise support, .NET integration

**Heroku**
- **Best for**: Quick MVPs (but expensive at scale)
- **Pricing**: $7/mo per dyno (now owned by Salesforce)
- **Pros**: Simple, Git-based deployment
- **Cons**: Expensive, less control

### Authentication

**Auth0** (Recommended)
- **Pricing**: Free up to 7000 users, $23/mo after
- **Pros**: Full-featured, social login, MFA, enterprise SSO
- **Cons**: Cost scales with users

**Firebase Auth**
- **Pricing**: Free (generous), $0.06 per verification beyond quota
- **Pros**: Simple, Google-backed, works with Firebase
- **Cons**: Vendor lock-in

**AWS Cognito**
- **Pricing**: Free tier 50K MAUs, then pay per use
- **Pros**: Integrates with AWS, scalable
- **Cons**: Complex UI, AWS lock-in

**Roll Your Own (JWT + bcrypt)**
- **Pros**: Full control, no vendor lock-in, free
- **Cons**: Security risk if done wrong, maintenance burden
- **Best for**: Experienced teams, very specific needs

### Payments

**Stripe** (Recommended)
- **Pricing**: 2.9% + $0.30 per transaction
- **Pros**: Developer-friendly API, comprehensive features
- **Best for**: SaaS, subscriptions, most startups

**PayPal**
- **Pricing**: 2.9% + $0.30 (similar to Stripe)
- **Pros**: Trusted brand, international
- **Cons**: Clunkier API, less developer-friendly

**Square**
- **Pricing**: 2.9% + $0.30 online
- **Pros**: Great for in-person + online
- **Best for**: Retail, physical products

### Email

**SendGrid**
- **Pricing**: Free 100 emails/day, $15/mo for 40K
- **Pros**: Reliable, good deliverability, templates

**Mailgun**
- **Pricing**: Free 5K emails/month, then pay-as-you-go
- **Pros**: Developer-friendly, good docs

**AWS SES**
- **Pricing**: $0.10 per 1000 emails (cheapest)
- **Pros**: Extremely cheap at scale
- **Cons**: More setup, AWS complexity

### Analytics

**Mixpanel**
- **Pricing**: Free up to 100K MTU, then $20/mo+
- **Best for**: Product analytics, user behavior

**Amplitude**
- **Pricing**: Free up to 10M events/month
- **Best for**: Product analytics, cohort analysis

**PostHog**
- **Pricing**: Free tier, self-hosted option
- **Best for**: Privacy-conscious, want to self-host

**Google Analytics**
- **Pricing**: Free
- **Best for**: Website traffic, marketing analytics
- **Cons**: Privacy concerns, less product-focused

## Hardware Stack

### Microcontrollers

**Arduino** (Beginner-Friendly)
- **Best for**: Simple prototypes, learning
- **Pros**: Huge community, tons of libraries, easy
- **Cons**: Limited performance, 8-bit
- **Price**: $20-40
- **Example Projects**: LED control, sensors, simple robotics

**Raspberry Pi** (Linux Computer)
- **Best for**: Complex applications, Linux needed
- **Pros**: Full Linux, GPIO, camera, WiFi
- **Cons**: Higher power consumption, more expensive
- **Price**: $35-75
- **Example Projects**: Home automation, media centers, AI edge

**ESP32** (WiFi/Bluetooth - Recommended)
- **Best for**: IoT devices, WiFi connectivity
- **Pros**: Cheap, WiFi+Bluetooth, low power
- **Cons**: More complex than Arduino
- **Price**: $5-15
- **Example Projects**: Smart home devices, sensors, wearables

**STM32** (Professional)
- **Best for**: Production hardware, advanced features
- **Pros**: Powerful, low power, ARM Cortex-M
- **Cons**: Steeper learning curve
- **Price**: $2-10 (in volume)
- **Example Projects**: Commercial products, medical devices

### Connectivity

**WiFi** (ESP32, Raspberry Pi)
- **Best for**: Home/office use, high data rates
- **Pros**: Fast, widely available
- **Cons**: Power hungry, limited range

**Bluetooth/BLE**
- **Best for**: Wearables, short-range communication
- **Pros**: Low power (BLE), simple pairing
- **Cons**: Limited range (30ft), lower data rate

**LoRa/LoRaWAN** (Long Range)
- **Best for**: Outdoor sensors, agricultural, smart cities
- **Pros**: Miles of range, low power
- **Cons**: Low data rate, licensing

**Cellular** (4G/5G)
- **Best for**: Remote monitoring, fleet tracking
- **Pros**: Global coverage, high reliability
- **Cons**: Monthly fees, power consumption

### Power

**USB-C PD** (Power Delivery)
- **Best for**: Desktop devices, high power needs
- **Pros**: Standardized, easy, ubiquitous
- **Cons**: Wired

**Lithium-Ion/LiPo Batteries**
- **Best for**: Portable devices
- **Pros**: High energy density, rechargeable
- **Cons**: Safety concerns, degradation
- **Capacity**: 1000-10000 mAh typical

**Solar**
- **Best for**: Remote sensors, outdoor devices
- **Pros**: Renewable, no battery replacement
- **Cons**: Inconsistent, requires battery backup

## Biotech Stack

### Lab Equipment

**Early Stage (R&D)**:
- PCR machine: $3K-10K
- Microplate reader: $5K-20K
- Centrifuge: $2K-8K
- Microscope: $5K-30K
- Pipettes: $200-500 each
- Freezers (-20°C, -80°C): $2K-10K

**Later Stage (Clinical/GMP)**:
- Flow cytometer: $50K-300K
- NGS sequencer: $100K-1M+
- Mass spectrometer: $300K-1M+
- Automated liquid handler: $30K-100K

### Reagents & Consumables

**Molecular Biology**:
- Enzymes (polymerases, restriction enzymes): $100-500/vial
- Antibodies: $300-600 per antibody
- Cell lines: $500-2000 per line
- Media and buffers: $50-200/liter

**Budget**: Plan $5K-20K/month in consumables for active R&D

### Analysis Software

**Bioinformatics**:
- **Free/Open Source**: BioPython, R/Bioconductor, Galaxy
- **Commercial**: Geneious ($1K-5K/year), MATLAB Bioinformatics Toolbox

**Statistics**:
- R / RStudio (free, most common)
- GraphPad Prism ($500-1000/year, user-friendly)
- SPSS ($100/month, enterprise)

**Data Management**:
- **LIMS** (Lab Information Management System): Benchling ($50-200/user/mo), LabWare
- **ELN** (Electronic Lab Notebook): Benchling, SciNote, LabArchives

### Regulatory Considerations

**FDA Pathway**:
- 510(k): $5K-50K (submission fees + consultants)
- PMA: $200K-500K+
- Timeline: 6-18 months (510k), 1-3 years (PMA)

**Quality Systems**:
- ISO 13485: Medical device quality management
- GMP (Good Manufacturing Practice): Pharma manufacturing
- CLIA: Clinical lab certification

## Decision Templates

### Build vs Buy

**When to Build**:
- Core competitive differentiator
- Specific requirements not met by existing tools
- Long-term cost savings justify upfront investment
- Need full control over data/roadmap

**When to Buy/SaaS**:
- Commodity functionality (auth, payments, email)
- Not core to your value proposition
- Faster time to market critical
- Ongoing maintenance burden too high

**Common "Buy" Decisions**:
- Authentication (Auth0, Firebase)
- Payments (Stripe, PayPal)
- Email (SendGrid, Mailgun)
- Analytics (Mixpanel, Amplitude)
- Error tracking (Sentry)
- Customer support (Intercom, Zendesk)

### Migration Path Planning

**Question**: Can you switch later if needed?

**Low Migration Risk** (Easy to switch):
- Databases (with ORM, schema migrations)
- Email providers (standard SMTP)
- Analytics (via Segment CDP)

**High Migration Risk** (Vendor lock-in):
- Firebase (entire backend)
- AWS Lambda (serverless architecture)
- Auth0 (user migration complex)

**Strategy**: Use abstraction layers for high lock-in risk services

## Recommendation Matrix

### For Different Startup Types

**SaaS Web App** (Most Common):
- **Frontend**: Next.js + React + Tailwind CSS
- **Backend**: Node.js (TypeScript) or Python (FastAPI)
- **Database**: PostgreSQL
- **Hosting**: Vercel (frontend) + Railway (backend+DB)
- **Auth**: Auth0 or Firebase Auth
- **Payments**: Stripe
- **Timeline**: 8-12 weeks to MVP

**Mobile App** (Consumer):
- **Mobile**: React Native or Flutter
- **Backend**: Firebase (for MVP) or custom API
- **Database**: Firestore or PostgreSQL
- **Hosting**: Firebase or AWS
- **Auth**: Firebase Auth
- **Analytics**: Mixpanel
- **Timeline**: 10-16 weeks to MVP

**IoT/Hardware**:
- **Microcontroller**: ESP32
- **Connectivity**: WiFi or BLE
- **Cloud**: AWS IoT Core or Azure IoT
- **Mobile App**: React Native
- **Database**: PostgreSQL + time-series (InfluxDB)
- **Timeline**: 6-12 months to market

**Biotech/Diagnostic**:
- **Lab Equipment**: Rent/lease initially
- **Analysis**: R + Bioconductor
- **LIMS**: Benchling
- **Regulatory**: Hire consultant ($5K-20K)
- **Timeline**: 2-4 years to market

**B2B SaaS** (Enterprise):
- **Frontend**: React + TypeScript
- **Backend**: Node.js or Go
- **Database**: PostgreSQL
- **Hosting**: AWS or Google Cloud
- **Auth**: Auth0 (SSO required for enterprise)
- **Monitoring**: DataDog
- **Timeline**: 12-20 weeks to MVP

## Cost Analysis

### Monthly Infrastructure Costs

**MVP (0-100 users)**:
- Hosting: $0-50 (Vercel free, Railway $5-20)
- Database: $0-25 (included in Railway/Supabase free tier)
- Auth: $0 (free tiers)
- Total: **$0-75/month**

**Growing (100-1000 users)**:
- Hosting: $100-300
- Database: $50-100
- Auth: $25-100
- Email: $15-50
- Analytics: $0-100
- Total: **$200-650/month**

**Scaling (1K-10K users)**:
- Hosting: $500-2000
- Database: $200-500
- Auth: $100-500
- Email: $50-200
- Analytics: $100-500
- Monitoring: $100-300
- Total: **$1000-4000/month**

## Checklist: Is Your Stack Solid?

- [ ] Team has expertise in chosen technologies (or can learn quickly)
- [ ] Tech stack supports MVP timeline (8-12 weeks for software)
- [ ] Scalable to 10x current users without major rewrite
- [ ] Budget aligned with projections
- [ ] Hiring feasible (can find developers for this stack)
- [ ] Ecosystem mature (libraries, tools, community)
- [ ] Migration path exists for high lock-in services
- [ ] Security best practices supported (HTTPS, encryption, etc.)
- [ ] Monitoring and error tracking in place
- [ ] Decision rationale documented

---

**Last Updated**: 2025-11-02
**Version**: 1.0.0
