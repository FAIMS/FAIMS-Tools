.null <null>
select uuid, attributename, attributeid, attributetype, valuetimestamp, vocabname, measure, freetext, certainty, appendcharacterstring as response
  from latestNonDeletedArchent
  join createdModifiedAtBy using (uuid)
  JOIN aenttype using (aenttypeid)
  JOIN idealaent using (aenttypeid)
  join attributekey using (attributeid)
  left outer join latestNonDeletedAentValue using (uuid, attributeid)
  left outer join user on (latestNonDeletedAentValue.userid = user.userid)
  left outer join vocabulary using (attributeid, vocabid)
  where uuid = (select uuid from latestnondeletedarchent limit 1)
  group by uuid, attributename
  order by AEntCountOrder, vocabcountorder;