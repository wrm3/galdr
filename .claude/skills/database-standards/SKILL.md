---
name: database-standards
description: Naming conventions, coding standards, and best practices for Oracle PL/SQL, MySQL, and PostgreSQL. Covers object naming, variable prefixes, parameter conventions, procedural code style, and schema design patterns. Use when writing SQL, PL/SQL, PL/pgSQL, stored procedures, DDL, or reviewing database code.
---

# Database Standards & Naming Conventions

Comprehensive standards for Oracle PL/SQL, MySQL, and PostgreSQL. Apply these conventions whenever writing, reviewing, or generating database code.

---

## Universal Rules (All Platforms)

### General Naming
- **snake_case** for all identifiers (tables, columns, variables, functions)
- **Lowercase only** — avoid quoted identifiers unless absolutely necessary
- **English only** — one spoken language throughout the schema
- **No reserved words** as identifiers — ever
- **No abbreviations** unless from a project glossary (e.g., `qty`, `amt`, `nbr`, `desc`)
- **3-63 characters** — descriptive but not unwieldy
- Names must start with a letter, never a digit
- No trailing spaces, no special characters (`$`, `#`, `@`) unless platform-required

### Boolean Columns
Use `is_`, `has_`, `can_`, `should_` prefixes:
```sql
is_active, has_children, can_edit, should_notify, is_deleted
```

### Timestamp Columns
Use `_at` suffix for timestamps, `_date` for date-only, `_on` for event dates:
```sql
created_at, updated_at, deleted_at, due_date, published_on
```

### Avoid
- Hungarian notation on tables/columns (`tbl_`, `col_`, `int_`)
- Meaningless names (`data`, `info`, `temp`, `value`, `item`)
- Pluralizing inconsistently (pick one convention per platform)
- Redundant table name in columns (`user_user_name` — just `user_name`)

---

## Oracle PL/SQL

### Schema Objects

| Object | Convention | Example |
|--------|-----------|---------|
| Table | singular noun, snake_case | `employee`, `order_line` |
| View | `v_` prefix | `v_active_employee` |
| Materialized View | `mv_` prefix | `mv_monthly_sales` |
| Sequence | `_seq` suffix | `employee_seq` |
| Index | `idx_table_column` | `idx_employee_last_name` |
| Primary Key | `pk_table` | `pk_employee` |
| Foreign Key | `fk_child_parent` | `fk_order_customer` |
| Unique Constraint | `uk_table_column` | `uk_employee_email` |
| Check Constraint | `ck_table_column` | `ck_employee_salary` |
| Trigger | `trg_table_action` | `trg_employee_before_insert` |
| Synonym | match the object name | `employee` (for `hr.employee`) |
| Type (Object) | `_type` suffix | `address_type` |
| Type (Collection) | `_tab_type` or `_list_type` | `employee_tab_type` |

### Package, Procedure, Function & Cursor Naming

| Object | Prefix | Convention | Example |
|--------|--------|-----------|---------|
| Package | `pack_` | `pack_module_purpose` | `pack_order_mgmt`, `pack_employee_api` |
| Procedure | `proc_` | `proc_verb_noun` | `proc_create_employee`, `proc_update_salary` |
| Function | `func_` | `func_descriptive_name` | `func_get_employee_name`, `func_calc_total` |
| Cursor | `cur_` | `cur_descriptive_name` | `cur_active_employees`, `cur_order_lines` |
| Spec file | `.pks` extension | | `pack_order_mgmt.pks` |
| Body file | `.pkb` extension | | `pack_order_mgmt.pkb` |

### Variable Prefixes (Scope + Type)

Variables use a compound prefix: **scope + type + `_`**

#### Local Variables

| Prefix | Meaning | Example |
|--------|---------|---------|
| `lvs_` | Local variable string | `lvs_employee_name`, `lvs_status_code` |
| `lvn_` | Local variable number | `lvn_total_amount`, `lvn_tax_rate` |
| `lvi_` | Local variable integer | `lvi_loop_counter`, `lvi_row_count` |
| `lvb_` | Local variable boolean | `lvb_is_valid`, `lvb_has_children` |
| `lvd_` | Local variable date | `lvd_hire_date`, `lvd_expiry_date` |
| `lvas_` | Local variable array of strings | `lvas_email_list`, `lvas_department_names` |
| `lvan_` | Local variable array of numbers | `lvan_salary_list`, `lvan_quantities` |
| `lvr_` | Local variable record | `lvr_employee`, `lvr_order_header` |

#### Local Constants

| Prefix | Meaning | Example |
|--------|---------|---------|
| `lcs_` | Local constant string | `lcs_default_status`, `lcs_error_prefix` |
| `lcn_` | Local constant number | `lcn_max_retries`, `lcn_tax_rate` |
| `lci_` | Local constant integer | `lci_batch_size`, `lci_max_rows` |
| `lcb_` | Local constant boolean | `lcb_debug_mode` |

#### Global (Package-Level) Variables

| Prefix | Meaning | Example |
|--------|---------|---------|
| `gvs_` | Global variable string | `gvs_application_name`, `gvs_current_user` |
| `gvn_` | Global variable number | `gvn_default_discount`, `gvn_conversion_rate` |
| `gvi_` | Global variable integer | `gvi_max_connections`, `gvi_retry_limit` |
| `gvb_` | Global variable boolean | `gvb_maintenance_mode`, `gvb_logging_enabled` |
| `gcs_` | Global constant string | `gcs_version`, `gcs_app_code` |
| `gcn_` | Global constant number | `gcn_pi`, `gcn_max_salary` |
| `gci_` | Global constant integer | `gci_max_batch_size` |

#### Parameters

| Prefix | Meaning | Example |
|--------|---------|---------|
| `p_in_` | IN parameter | `p_in_employee_id`, `p_in_department_name` |
| `p_out_` | OUT parameter | `p_out_total_count`, `p_out_error_msg` |
| `p_io_` | IN OUT parameter | `p_io_running_total`, `p_io_status` |

#### Other Prefixes

| Prefix/Suffix | Type | Example |
|---------------|------|---------|
| `e_` prefix | User exception | `e_duplicate_entry`, `e_not_found` |
| `_type` suffix | Type definition | `employee_rec_type`, `id_list_type` |

### Procedure & Function Examples

```sql
-- Procedures: proc_ prefix + verb_noun
procedure proc_create_employee(p_in_name in varchar2, p_out_id out number);
procedure proc_update_salary(p_in_employee_id in number, p_in_new_salary in number);
procedure proc_delete_order_line(p_in_line_id in number);
procedure proc_process_payroll(p_in_period_date in date);

-- Functions: func_ prefix + descriptive name
function func_get_employee_name(p_in_id in number) return varchar2;
function func_calc_total_salary(p_in_dept_id in number) return number;
function func_is_eligible_for_bonus(p_in_employee_id in number) return boolean;
function func_find_next_sequence return number;
```

### PL/SQL Code Style

```sql
create or replace package body pack_order_mgmt as

  gci_max_retry_count constant pls_integer := 3;
  gcs_module_name     constant varchar2(30) := 'pack_order_mgmt';

  function func_get_order_total(p_in_order_id in number) return number is
    lvn_total       number := 0;
    lvn_tax_rate    number;
    lvn_discount    number;

    cur_order_lines cursor is
      select quantity, unit_price, discount_pct
        from order_line
       where order_id = p_in_order_id;
  begin
    for lvr_line in cur_order_lines loop
      lvn_discount := lvr_line.unit_price * nvl(lvr_line.discount_pct, 0);
      lvn_total := lvn_total + (lvr_line.quantity * (lvr_line.unit_price - lvn_discount));
    end loop;

    lvn_tax_rate := func_get_tax_rate(p_in_order_id);
    lvn_total := lvn_total * (1 + lvn_tax_rate);

    return lvn_total;
  exception
    when no_data_found then
      return 0;
    when others then
      proc_log_error(gcs_module_name, 'func_get_order_total', sqlerrm);
      raise;
  end func_get_order_total;

end pack_order_mgmt;
/
```

### Oracle Case Rule

**All PL/SQL identifiers**: lowercase. **SQL keywords** (SELECT, FROM, WHERE, BEGIN, END, etc.): UPPERCASE for readability.

```sql
-- CORRECT
CREATE OR REPLACE PACKAGE BODY api-gateway.pack_account AS
    PROCEDURE proc_get_balance(
        p_in_account_id    IN  VARCHAR2,
        p_out_balance      OUT NUMBER
    ) AS
        lvn_balance  NUMBER;
    BEGIN
        SELECT balance INTO lvn_balance
          FROM account
         WHERE account_id = p_in_account_id;
        p_out_balance := lvn_balance;
    END proc_get_balance;
END pack_account;
/

-- WRONG — never write this
CREATE OR REPLACE PACKAGE BODY api-gateway.PKG_ACCOUNT AS
    PROCEDURE GET_BALANCE(P_CUENTA IN VARCHAR2, P_SALDO OUT NUMBER) AS
        lv_saldo  NUMBER;
    BEGIN ...
```

### Spanish → English Translation Reference

All **new code** must use English identifiers. When encountering legacy Spanish names, translate:

| Wrong (Spanish) | Right (English) |
|---|---|
| `p_in_empresa` | `p_in_company_code` |
| `p_in_agencia` | `p_in_branch_code` |
| `p_in_numero_cuenta` | `p_in_account_number` |
| `p_out_saldo` | `p_out_balance` |
| `lvs_situacion` | `lvs_status` |
| `lvn_dias_mora` | `lvn_days_overdue` |
| `PKG_CUENTA` | `pack_account` |
| `PROC_OBTENER_SALDO` | `proc_get_balance` |

### Standard Error Handling Pattern

All procedures that communicate errors to callers should use this pattern:

```sql
PROCEDURE proc_get_balance(
    p_in_account_id    IN  VARCHAR2,
    p_out_balance      OUT NUMBER,
    p_out_error_code   OUT NUMBER,
    p_out_error_msg    OUT VARCHAR2
) AS
    lvn_balance  NUMBER;
BEGIN
    SELECT balance INTO lvn_balance
      FROM account
     WHERE account_id = p_in_account_id;

    p_out_balance    := lvn_balance;
    p_out_error_code := 0;
    p_out_error_msg  := NULL;
EXCEPTION
    WHEN no_data_found THEN
        p_out_error_code := -1;
        p_out_error_msg  := 'Record not found';
    WHEN OTHERS THEN
        p_out_error_code := SQLCODE;
        p_out_error_msg  := SUBSTR(SQLERRM, 1, 500);
END proc_get_balance;
```

### Oracle Pre-Commit Checklist

Before committing Oracle PL/SQL code, verify:
- [ ] Package starts with `pack_` (not `PKG_`)
- [ ] All procedures start with `proc_` (not bare verbs)
- [ ] All functions start with `func_`
- [ ] All cursors start with `cur_`
- [ ] IN params start with `p_in_`
- [ ] OUT params start with `p_out_`
- [ ] IN OUT params start with `p_io_`
- [ ] Local vars use `lvs_`/`lvn_`/`lvd_`/`lvi_`/`lvb_`/`lvr_`/`lvas_`
- [ ] All new identifiers are in **English**
- [ ] All identifiers are **lowercase**
- [ ] SQL keywords are **UPPERCASE**
- [ ] Spec file uses `.pks`, body uses `.pkb`
- [ ] Error handling follows the `p_out_error_code`/`p_out_error_msg` pattern

### Oracle Best Practices
- Declare cursors in package spec, define queries in package body
- Use `%type` and `%rowtype` to anchor variable types to table columns
- Never use `select *` — always name columns explicitly
- Initialize variables in the body's initialization block, not inline, when exceptions are possible
- Use `bulk collect` and `forall` for batch operations (never row-by-row in loops)
- Always include an `exception` block — at minimum log and re-raise
- Use `accessible by` clause to restrict package access
- Limit package spec to only what callers need — hide internals in body
- Use `pls_integer` over `number` for loop counters and integer math
- Bind variables, never string concatenation for dynamic SQL

---

## MySQL

### Schema Objects

| Object | Convention | Example |
|--------|-----------|---------|
| Table | singular noun, snake_case | `customer`, `order_item` |
| View | `v_` prefix | `v_active_customer` |
| Temporary Table | `tmp_` prefix | `tmp_import_staging` |
| Index | `idx_table_column` | `idx_customer_email` |
| Primary Key | `pk_table` | `pk_customer` |
| Foreign Key | `fk_child_parent` | `fk_order_customer` |
| Unique Index | `uq_table_column` | `uq_customer_email` |
| Check Constraint | `ck_table_column` | `ck_order_total` |
| Trigger | `trg_table_timing_action` | `trg_customer_before_insert` |
| Event | `evt_purpose` | `evt_nightly_cleanup` |
| Junction Table | `table1_table2` | `student_course` |

### Stored Procedure & Function Naming

```sql
-- Procedures: verb_noun (sp_ prefix optional but consistent)
create procedure create_customer(in p_name varchar(100), in p_email varchar(255))
create procedure update_order_status(in p_order_id int, in p_status varchar(20))
create procedure delete_expired_session()
create procedure process_daily_report(in p_report_date date)

-- Functions: return-focused
create function get_customer_name(p_customer_id int) returns varchar(100)
create function calc_order_total(p_order_id int) returns decimal(10,2)
create function is_valid_email(p_email varchar(255)) returns boolean
```

### Variable Naming

| Prefix | Scope | Example |
|--------|-------|---------|
| `p_` | Parameter | `p_customer_id`, `p_order_date` |
| `v_` | Local variable | `v_count`, `v_total_amount` |
| `@` | Session/user variable | `@session_user_id` |
| `@@` | System variable (read-only) | `@@version` |

### MySQL Code Style

```sql
create procedure process_order(
  in  p_order_id   int,
  in  p_customer_id int,
  out p_total      decimal(10,2)
)
begin
  declare v_item_count   int default 0;
  declare v_subtotal     decimal(10,2) default 0.00;
  declare v_tax_rate     decimal(5,4);
  declare v_done         boolean default false;

  declare item_cur cursor for
    select quantity, unit_price
      from order_item
     where order_id = p_order_id;

  declare continue handler for not found set v_done = true;

  select tax_rate into v_tax_rate
    from customer
   where customer_id = p_customer_id;

  open item_cur;
  read_loop: loop
    fetch item_cur into v_quantity, v_price;
    if v_done then
      leave read_loop;
    end if;
    set v_subtotal = v_subtotal + (v_quantity * v_price);
    set v_item_count = v_item_count + 1;
  end loop;
  close item_cur;

  set p_total = v_subtotal * (1 + coalesce(v_tax_rate, 0));
end;
```

### MySQL Best Practices
- Use `InnoDB` engine for all tables (ACID compliance, row-level locking)
- Always define a primary key — prefer `bigint auto_increment`
- Use `utf8mb4` charset and `utf8mb4_unicode_ci` collation (not `utf8`)
- Use `decimal` for money, never `float` or `double`
- Always use parameterized queries — never concatenate user input
- Use `coalesce()` over `ifnull()` for portability
- Declare `exit handler` and `continue handler` for error management
- Use `signal sqlstate` for custom error raising
- Limit stored procedure length — decompose into helper procedures
- Use `explain` to verify query plans before deploying

---

## PostgreSQL

### Schema Objects

| Object | Convention | Example |
|--------|-----------|---------|
| Table | **plural** nouns, snake_case | `customers`, `order_items` |
| View | `v_` prefix | `v_active_customers` |
| Materialized View | `mv_` prefix | `mv_monthly_revenue` |
| Sequence | `_seq` suffix | `customers_seq` |
| Index | `idx_table_column` | `idx_customers_email` |
| Primary Key | `_pkey` suffix | `customers_pkey` |
| Foreign Key | `_fkey` suffix | `order_items_order_id_fkey` |
| Unique Constraint | `_key` suffix | `customers_email_key` |
| Check Constraint | `_check` suffix | `orders_total_check` |
| Exclusion Constraint | `_excl` suffix | `booking_period_excl` |
| Trigger | `trg_table_action` | `trg_customers_updated_at` |
| Schema | business domain name | `billing`, `inventory`, `auth` |
| Enum Type | singular, `_status` or `_type` | `order_status`, `payment_type` |
| Domain | `d_` prefix or descriptive | `d_email`, `d_positive_int` |
| Extension | lowercase | `pgcrypto`, `pg_trgm` |

**Note**: PostgreSQL convention uses **plural** table names (unlike Oracle/MySQL singular). This is the community standard — tables represent collections of rows.

### Function & Procedure Naming

```sql
-- Functions: verb_noun
create function get_customer_name(_customer_id bigint) returns text
create function calc_order_total(_order_id bigint) returns numeric
create function is_active_subscription(_sub_id bigint) returns boolean
create function find_duplicate_emails() returns setof text

-- Procedures (PG 11+): action verbs
create procedure process_refund(_order_id bigint, _amount numeric)
create procedure archive_old_orders(_before_date date)
create procedure sync_inventory(_warehouse_id int)
```

### Variable & Parameter Naming

| Prefix | Scope | Example |
|--------|-------|---------|
| `_` | Function/procedure parameter | `_customer_id`, `_order_date` |
| `v_` | Local variable (DECLARE block) | `v_count`, `v_total` |
| (none) | Column reference (in queries) | `customer_id`, `email` |

The underscore prefix for parameters is critical in PostgreSQL — it prevents ambiguity between parameter names and column names in SQL statements within the function body.

### PL/pgSQL Code Style

```sql
create or replace function calc_invoice_total(
  _invoice_id  bigint,
  _include_tax boolean default true
)
returns numeric
language plpgsql
stable
as $$
declare
  v_subtotal   numeric := 0;
  v_tax_rate   numeric;
  v_total      numeric;
begin
  select sum(quantity * unit_price)
    into v_subtotal
    from invoice_items
   where invoice_id = _invoice_id;

  if v_subtotal is null then
    return 0;
  end if;

  if _include_tax then
    select coalesce(c.default_tax_rate, 0)
      into v_tax_rate
      from invoices i
      join customers c on c.customer_id = i.customer_id
     where i.invoice_id = _invoice_id;

    v_total := v_subtotal * (1 + v_tax_rate);
  else
    v_total := v_subtotal;
  end if;

  return round(v_total, 2);
end;
$$;
```

### PostgreSQL Best Practices
- Use `bigint` or `bigserial` for primary keys (not `serial`/`int` — you will run out)
- Use `text` over `varchar` when no length constraint is needed
- Use `numeric` for money, never `float` or `real`
- Use `timestamptz` (with time zone) over `timestamp` — always
- Use schemas to organize domain boundaries (`auth.users`, `billing.invoices`)
- Declare function volatility: `immutable`, `stable`, or `volatile`
- Use `returns table(...)` for functions returning result sets
- Always prefix parameters with `_` to avoid column name ambiguity
- Use `raise notice` for debugging, `raise exception` for errors
- Use `perform` instead of `select` when discarding results
- Use `found` variable after `select into` to check for no-data
- Prefer `exists()` over `count(*) > 0`
- Use `returning` clause on INSERT/UPDATE/DELETE to avoid extra queries
- Use CTEs (`with`) for complex queries — readability over micro-optimization
- Always use `if not exists` / `if exists` in DDL for idempotency

---

## Cross-Platform Quick Reference

### Table Names
| Platform | Convention | Example |
|----------|-----------|---------|
| Oracle | Singular | `employee` |
| MySQL | Singular | `customer` |
| PostgreSQL | **Plural** | `customers` |

### Variable & Parameter Prefixes
| Platform | IN Param | OUT Param | Local String | Local Number | Local Integer | Global Var |
|----------|----------|-----------|--------------|--------------|---------------|------------|
| Oracle | `p_in_` | `p_out_` | `lvs_` | `lvn_` | `lvi_` | `gv*_` |
| MySQL | `p_` | `p_` (with `out`) | `v_` | `v_` | `v_` | `@var` |
| PostgreSQL | `_` prefix | `_` prefix (with `out`) | `v_` | `v_` | `v_` | N/A |

### Object Prefixes (Oracle-Specific)
| Object | Prefix | Example |
|--------|--------|---------|
| Package | `pack_` | `pack_order_mgmt` |
| Procedure | `proc_` | `proc_create_employee` |
| Function | `func_` | `func_get_total` |
| Cursor | `cur_` | `cur_active_employees` |

### Primary Key Column
| Platform | Convention | Example |
|----------|-----------|---------|
| Oracle | `id` or `table_id` | `employee_id` |
| MySQL | `id` or `table_id` | `customer_id` |
| PostgreSQL | `table_id` (singular) | `customer_id` |

### Money/Decimal
| Platform | Type | Never Use |
|----------|------|-----------|
| Oracle | `number(p,s)` | `float`, `binary_float` |
| MySQL | `decimal(p,s)` | `float`, `double` |
| PostgreSQL | `numeric(p,s)` | `real`, `double precision` |

### Timestamps
| Platform | Type |
|----------|------|
| Oracle | `timestamp with time zone` |
| MySQL | `datetime` or `timestamp` |
| PostgreSQL | `timestamptz` (always) |

---

## DDL Template Examples

### Oracle
```sql
create table employee (
  employee_id    number        generated always as identity,
  first_name     varchar2(100) not null,
  last_name      varchar2(100) not null,
  email          varchar2(255) not null,
  hire_date      date          not null,
  salary         number(10,2),
  department_id  number,
  is_active      number(1)     default 1 not null,
  created_at     timestamp with time zone default systimestamp not null,
  updated_at     timestamp with time zone,
  constraint pk_employee primary key (employee_id),
  constraint uk_employee_email unique (email),
  constraint fk_employee_department foreign key (department_id)
    references department(department_id),
  constraint ck_employee_salary check (salary >= 0)
);

create index idx_employee_department on employee(department_id);
create index idx_employee_last_name on employee(last_name);
```

### MySQL
```sql
create table customer (
  customer_id  bigint        auto_increment,
  first_name   varchar(100)  not null,
  last_name    varchar(100)  not null,
  email        varchar(255)  not null,
  signup_date  date          not null,
  balance      decimal(10,2) default 0.00,
  is_active    tinyint(1)    default 1 not null,
  created_at   datetime      default current_timestamp not null,
  updated_at   datetime      default current_timestamp on update current_timestamp,
  constraint pk_customer primary key (customer_id),
  constraint uq_customer_email unique (email),
  constraint ck_customer_balance check (balance >= 0)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create index idx_customer_last_name on customer(last_name);
```

### PostgreSQL
```sql
create table customers (
  customer_id  bigint        generated always as identity,
  first_name   text          not null,
  last_name    text          not null,
  email        text          not null,
  signup_date  date          not null default current_date,
  balance      numeric(10,2) default 0.00,
  is_active    boolean       default true not null,
  created_at   timestamptz   default now() not null,
  updated_at   timestamptz,
  constraint customers_pkey primary key (customer_id),
  constraint customers_email_key unique (email),
  constraint customers_balance_check check (balance >= 0)
);

create index idx_customers_last_name on customers(last_name);
```

---

## Migration & DDL Best Practices

- Always use `if not exists` / `if exists` for idempotent DDL
- Add columns as `nullable` first, backfill, then add `not null` constraint
- Never rename columns in production without a migration plan (add new, copy, drop old)
- Always include `created_at` and `updated_at` on every table
- Foreign key columns should match the referenced column name exactly
- Index foreign key columns — databases do not auto-index FK columns (except MySQL InnoDB)
- Use database-native sequences or identity columns — never application-generated IDs for primary keys
- Comment tables and columns with business definitions:
  ```sql
  comment on table customers is 'Registered platform users with billing accounts';
  comment on column customers.balance is 'Current account balance in USD, updated by billing service';
  ```
