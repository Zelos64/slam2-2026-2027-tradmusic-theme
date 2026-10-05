<?php

namespace App\DataFixtures;

use App\Entity\City;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;

class CityFixtures extends Fixture
{
    public function load(ObjectManager $manager): void
    {
        $cities = [
            'Dublin',
            'Cork',
            'Galway',
            'Limerick',
            'Waterford',
            'Belfast',
            'Derry',
            'Sligo',
            'Kilkenny',
            'Killarney'
        ];

        foreach ($cities as $cityName) {
            $city = new City();
            $city->setName($cityName);
            $manager->persist($city);
        }

        $manager->flush();
    }
}