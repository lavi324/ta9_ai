[[_TOC_]]
# Intro
In microservices applications there's an ongoing need to create objects from other objects which are (sometimes) quite similar.
For example, convert an ApiModel object to a Domain entity object.
We don't want to manually copy object's contents to another one every time we're doing that so we're using a dedicated framework for that which enables us to easily map one object to another.

# AutoMapper
_AutoMapper_ is an easy-to-use framework allows us to map/copy/convert one object to another.
_AutoMapper_ maps by default objects' properties by name.
_AutoMapper_ has a fluent API for defining mapping conditions/instructions.
_AutoMapper_ has a great documentation here.

# Developer Guide
1. Add _nuget_ packages (use same version as used in _Solution_):
1.1 `AutoMapper`
1.2 `AutoMapper.Extensions.Microsoft.DependencyInjection`
1. Defining the _Mapper_ 
2.1 Create a _Mapping Profile_ class & locate it on folder `Infrastructure/AutoMapper` within the project
2.2 Name the class just `MappingProfile` (unless there's a bunch of logically-connected mappings than can be splitted to multiple profiles) 
2.3 In the profile _constructor_, create mapping/s between the objects that are used, e.g
            `CreateMap<ScheduledTask, ExecuteScheduledTaskJob>();`
2.3.1 In this simple sample, all the properties of the same name & type will be copied
2.3.2 If we need a more advanced _mapping_ (e.g - change type) we can do that by _AutoMapper_'s fluent API extension methods, e.g:
            
```
CreateMap<AddScheduledTask, ScheduledTask>().ForMember(x => x.TimeOfDay, o => o.MapFrom(s => new TimeSpan(s.TimeOfDayHour, s.TimeOfDayMinute, 0)))
                                            .ForMember(x => x.Timezone, o => o.MapFrom(s => tzConverter.GetTimeZoneFromString(s.Timezone)));
```

3. Using the Mapper
3.1 _Inject_ the _Mapper_ to wherever you need:
        
```
private IMapper _mapper;
public ScheduledTasksController(IMapper mapper)
{
  _mapper = mapper;
}
```

3.2 Use the _mapper_ to map between actual objects:
`_mapper.Map<ExecuteScheduledTaskJob>(request.TaskToProcess)ntro`