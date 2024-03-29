create schema youtube;
use youtube;

create table channel(
channel_id varchar(100),
channel_name varchar(100),
upload_id varchar(100),
channel_type varchar(100),
channel_views bigint,
channel_description text,
channel_status varchar(100),
channel_created datetime,
channel_subscribers int,
video_count int
);

create table playlist(
channel_id varchar(100),
playlist_id varchar(100),
playlist_name varchar(100),
video_count int,
first_upload_date datetime
);

create table comment(
comment_id varchar(100),
video_id varchar(100),
commenter_name varchar(100),
comment_text text,
commented_time datetime
);
create table video_table(
channel_id varchar(100),
video_id varchar(100),
video_name varchar(100),
video_description text,
video_published_on datetime,
video_views int,
video_likes int,
video_dislikes int,
video_favourite int,
video_comments int,
duration time,
thumbnail varchar (1024),
caption_status varchar(20)
);

#1
Select v.video_name as "video name", c.channel_name as "channel name" from video_table as v left join channel as c on c.channel_id =v.channel_id;

#2
Select channel_name as "channel name" , video_count as "Number of videos" from channel order by video_count desc;

#3
Select c.channel_name as "channel name" , v.video_name as "Video name" , v.video_views as "Number of views" from video_table as v left join channel as c 
on v.channel_id = c.channel_id order by v.video_views desc limit 10;

#4
Select video_name as "Video Name" , video_comments as "Number of comments" from video_table;

#5
Select c.channel_name as "Channel name" , v.video_name as "Video name" , v.video_likes as "Number of likes" from video_table as v left join channel as c 
on c.channel_id = v.channel_id order by video_likes desc limit 10;

#6
Select video_name as "Video name" , video_likes as "Number of likes" from video_table;

#7
Select channel_name as "Channel name" , channel_views as "Number of views" from channel;

#8
select c.channel_name as "Channel name" , count(v.video_id) as "Video count" 
from video_table as v left join channel as c on v.channel_id = c.channel_id
where year(video_published_on) = 2022
group by c.channel_name;


#9
Select c.channel_name as "Channel name", sec_to_time(avg( time_to_sec (v.duration) )) as "Average duration" 
from video_table as v left join channel as c on v.channel_id = c.channel_id
group by v.channel_id, c.channel_name;


#10
Select c.channel_name , v.video_name, v.video_comments from video_table as v left join channel as c
on c.channel_id= v.channel_id 
order by v.video_comments desc limit 10;

