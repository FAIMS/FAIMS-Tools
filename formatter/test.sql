  select uuid, aenttypeid, aenttypename, group_concat(coalsece(formatstring, vocabname, measure, freetext, certainty), appendcharacterstring) as response, null as deleted
  from latestNonDeletedArchent 
  JOIN aenttype using (aenttypeid)
  JOIN idealaent using (aenttypeid)
  join attributekey using (attributeid)
  join latestNonDeletedAentValue using (uuid, attributeid)  
  left outer join vocabulary using (attributeid, vocabid)
 WHERE isIdentifier = 'true'
 group by uuid, attributeid
 order by uuid, aentcountorder;
