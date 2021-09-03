from grafanalib.core import *
from grafanalib.influxdb import InfluxDBTarget

dashboard = Dashboard(
    title="Metrics",
    templating=
        Templating([
            Template(
                name='vehicle',
                query="select DISTINCT(vehicle) from metrics where notEmpty(timer_latencies) order by vehicle",
                label='vehicle',
                sort=0,
                default='paccar-amazonph4-k003dm',
            ),
            Template(
                name='trip',
                query="select DISTINCT(trip) from metrics where notEmpty(timer_latencies)  and vehicle in (${vehicle:sqlstring}) order by trip",
                label='trip',
                sort=0,
            ),
            Template(
                name='build_commit',
                query="select DISTINCT(group) from metrics where notEmpty(timer_latencies)  and trip in (${trip:sqlstring}) order by ts",
                label='build_commit',
                sort=0,
                default='All',
                includeAll=True,
                multi=True,
            ),
            Template(
                name='bag_name',
                query="select DISTINCT(bag_name) from metrics where notEmpty(timer_latencies) and trip in (${trip:sqlstring}) and group in (${build_commit:sqlstring}) order by ts",
                label='bag_name',
                sort=0,
                default='All',
                includeAll=True,
                multi=True,
            ),
            Template(
                name='node',
                query="select DISTINCT(node) from metrics where notEmpty(timer_latencies) and bag_name in (${bag_name:sqlstring}) order by node",
                label='NODE',
                sort=0,
                default=["controller_ros_node", "fusion_object_tracker","lane_detector", "prediction", "scenario_planner"],
                multi=True,
            ),
            Template(
                name='timer',
                query="""SELECT
    distinct(JSONExtractString(l, 'name')) as name
FROM
    metrics array join JSONExtractArrayRaw(assumeNotNull(timer_latencies), 'timers') as l
WHERE
    notEmpty(timer_latencies) and node in (${node:sqlstring}) and bag_name in (${bag_name:sqlstring})
order by
    name""",
                label='TIMER',
                sort=0,
                default=["ControlWorker::Run", "FusionTrackerRuntimeInterface::processFusedSensorMessages", "PublishWorker::Run", "scoped_timer.lane_detector_by_image", "scoped_timer.prediction_update_obstacle", "scoped_timer.process_image", "PlanningRosWrapper::onTimer"],
                multi=True,
            ),
        ]),
    panels=[
        Graph(
            title="$timer",
            dataSource='ClickHouse',
            targets=[
                InfluxDBTarget(
                    query="""SELECT
    ts as t,
    JSONExtractFloat(l, 'P50') as P50,
    JSONExtractFloat(l, 'P95') as P95,
    JSONExtractFloat(l, 'P99') as P99,
    JSONExtractFloat(l, 'avg_time_ms') as Average
FROM metrics array join JSONExtractArrayRaw(assumeNotNull(timer_latencies), 'timers') as l
WHERE 
    JSONExtractString(l,'name') in (${timer:sqlstring}) and notEmpty(timer_latencies)
    and bag_name in (${bag_name:sqlstring}) and node in (${node:sqlstring})

ORDER by t""",
                    refId='A',
                ),
            ],
            yAxes=single_y_axis(format=MILLISECONDS_FORMAT, min=None),
            gridPos=GridPos(h=8, w=24, x=0, y=0),
            maxDataPoints=None,
            repeat=Repeat(direction='v', variable='timer'),
            lineWidth=1,
            pointRadius=1,
            points=True,
        )
    ],
    time=Time(
            start="2021-08-05T19:53:03.794Z",
            end="2021-08-06T00:49:17.000Z"
         ),
    timezone='America/Los_Angeles',
).auto_panel_ids()
