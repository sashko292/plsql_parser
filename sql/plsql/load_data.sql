-- Task Table Transformation
create table bidevtasklist.task_tmp2 as
select distinct task_key,
                summary,
                assignee,
                sprint,
                parent_key,
                components,
                epic,
                labels,
                original_estimate,
                total_time_spent,
                status,
                type,
                resolution_date,
                created_date,
                updated_date,
                project
from (select task_key,
             summary,
             assignee,
             sprint,
             parent_key,
             components,
             epic,
             labels,
             original_estimate,
             total_time_spent,
             status,
             type,
             resolution_date,
             created_date,
             updated_date,
             project,
             src,
             min(src) over (partition by task_key) as min_src
      from (select task_key,
                   summary,
                   assignee,
                   sprint,
                   parent_key,
                   components,
                   epic,
                   labels,
                   original_estimate,
                   total_time_spent,
                   status,
                   type,
                   resolution_date,
                   created_date,
                   updated_date,
                   project,
                   2 as src
            from bidevtasklist.task t
            union all
            select task_key,
                   summary,
                   assignee,
                   sprint,
                   parent_key,
                   components,
                   epic,
                   labels,
                   original_estimate,
                   total_time_spent,
                   status,
                   type,
                   resolution_date,
                   created_date,
                   updated_date,
                   project,
                   1 as src
            from bidevtasklist.task_tmp t) t) t
where t.src = t.min_src;

drop table bidevtasklist.task;

alter table bidevtasklist.task_tmp2
    rename to task;

-- Worklog Table Transformation
create table bidevtasklist.worklog_tmp2 as
select distinct task_key,
                user,
                log_date,
                total_time_spent
from (select task_key,
             user,
             log_date,
             total_time_spent,
             src,
             min(src) over (partition by task_key, user, log_date) as min_src
      from (select task_key,
                   user,
                   log_date,
                   total_time_spent,
                   2 as src
            from bidevtasklist.worklog
            union all
            select task_key,
                   user,
                   log_date,
                   total_time_spent,
                   1 as src
            from bidevtasklist.worklog_tmp) t) t
where t.src = t.min_src;

drop table bidevtasklist.worklog;

alter table bidevtasklist.worklog_tmp2
    rename to worklog;

-- Link Table Transformation
create table bidevtasklist.link_tmp2 as
select distinct current_task_key,
                related_task_key,
                link_type
from (select current_task_key,
             related_task_key,
             link_type,
             src,
             min(src) over (partition by current_task_key, related_task_key, link_type) as min_src
      from (select current_task_key,
                   related_task_key,
                   link_type,
                   2 as src
            from bidevtasklist.link
            union all
            select current_task_key,
                   related_task_key,
                   link_type,
                   1 as src
            from bidevtasklist.link_tmp) t) t
where t.src = t.min_src;

drop table bidevtasklist.link;

alter table bidevtasklist.link_tmp2
    rename to link;

-- Transition Table Transformation
create table bidevtasklist.transition_tmp2 as
select distinct task_key,
                username,
                transition_date,
                status
from (select task_key,
             username,
             transition_date,
             status,
             src,
             min(src) over (partition by task_key, username, transition_date) as min_src
      from (select task_key,
                   username,
                   transition_date,
                   status,
                   2 as src
            from bidevtasklist.transition
            union all
            select task_key,
                   username,
                   transition_date,
                   status,
                   1 as src
            from bidevtasklist.transition_tmp) t) t
where t.src = t.min_src;

drop table bidevtasklist.transition;

alter table bidevtasklist.transition_tmp2
    rename to transition;